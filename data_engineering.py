#!/usr/bin/env python

import os
import time

import boto3
from botocore.exceptions import ClientError

import utils
from config import app_config
from database_manager.db_error import DBError
from database_manager.db_manager import db_manager
from pipeline.pipeline_error import PipelineError
from pipeline.pipeline_factory import PipelineFactory
from static import constants as const
from static.status import Status
from study.study import InvalidStudyError
from study.study import Study

LOGGER_NAME = 'data_engineering'


class DataEngineering:
    """
    Represents the Data Engineering Module.
    """
    def __init__(self):
        self.logger = None

    def setup(self, config_file_name):
        """
        Set up the configuration, logger, and db manager.
        """
        try:
            app_config.setup(config_file_name)
        except FileExistsError as e:
            raise ValueError(e)

        self.logger = utils.setup_logger(logger_name=LOGGER_NAME, logging_level=app_config.logging_level)

        try:
            db_manager.setup(app_config)
        except DBError as e:
            raise ValueError(e)

    def run(self):
        """
        Constantly crawl the given directory to find downloaded studies. Process all studies that are ready to be
        processed.
        """
        directory = app_config.input_path

        # Validate the directory.
        if directory is None or not os.path.isdir(directory):
            raise ValueError(f'{directory} is not a valid directory.')

        print(f'Monitoring {directory}')
        while True:
            for root, sub_dirs, file_names in os.walk(directory):
                if Study.is_ready_for_processing(file_names):
                    # Claim the study
                    try:
                        utils.create_txt(file_path=os.path.join(root, const.CLAIMED_MARKER))
                    except ValueError:
                        continue

                    # Process the study
                    self.process_study(root)
            time.sleep(3)

    def process_study(self, directory):
        """
        Create a study from the user provided directory. Then create a Qiime2 pipeline and execute it.
        """
        # Check if the claimed marker belongs to this process
        if not utils.is_file_owned_by_me(file_path=os.path.join(directory, const.CLAIMED_MARKER)):
            return

        start_time = time.time()

        study_id = os.path.basename(directory)

        # Update the status and retrieve attributes using the run ID.
        try:
            db_manager.update_status(run_id=study_id, status=Status.PROCESSING)
            user_id = db_manager.get_user_id(run_id=study_id)
            email = db_manager.get_email(run_id=study_id)
            email_notification = db_manager.get_email_notification_preference(run_id=study_id)
            is_public = db_manager.is_run_public(run_id=study_id)
        except DBError as e:
            self.error_out(study_id=study_id, error_msg=str(e), directory=directory)
            return

        self.logger.debug(f'Processing {study_id}')
        study = Study(parent_dir=directory, user_id=user_id, is_public=is_public)
        try:
            study.setup()
        except InvalidStudyError as e:
            self.error_out(study_id=study_id, error_msg=str(e), directory=directory)
            return

        self.logger.debug(f'{study.id} | Generating a Qiime2 pipeline.')
        try:
            pipeline = PipelineFactory.generate_pipeline(study, LOGGER_NAME)
        except InvalidStudyError as e:
            self.error_out(study_id=study_id, error_msg=str(e), directory=directory)
            return

        self.logger.debug(f'{study.id} | Executing the pipeline.')
        try:
            pipeline.execute()
        except PipelineError as e:
            self.error_out(study_id=study_id, error_msg=str(e), directory=directory)
            return

        self.logger.debug(f'{study.id} | Creating the results csv file.')
        try:
            results_csv_path = utils.create_results_csv(study_id=study_id,
                                                        feature_table_path=pipeline.get_feature_table_path(),
                                                        taxonomy_results_path=pipeline.get_taxonomy_results_path(),
                                                        output_dir=pipeline.get_output_dir())
        except ValueError as e:
            self.error_out(study_id=study_id, error_msg=str(e), directory=directory)
            return

        # Post the results
        try:
            db_manager.post_results(csv_path=results_csv_path)
            self.logger.info(f'{study.id} | Sent results to the database successfully.')
        except DBError as e:
            self.error_out(study_id=study_id, error_msg=str(e), directory=directory)
            return

        self.logger.info(f'{study.id} | Process Completed. Runtime: {utils.get_runtime(start_time)}')

        try:
            db_manager.update_status(run_id=study_id, status=Status.SUCCESS, output_path=pipeline.get_output_dir())
        except DBError as e:
            self.error_out(study_id=study_id, error_msg=str(e), directory=directory)
            return

        # Clean up
        self.remove_input_dir(directory)

        # Inform the client
        if email and email_notification:
            self.send_email(recipient=email, run_id=study_id)

    def error_out(self, study_id, error_msg, directory):
        """
        Log the error message, create an error text file, and update the status table.
        """
        self.logger.error(f'{study_id} | {error_msg}')
        utils.create_txt(file_path=os.path.join(directory, const.ERROR_MARKER), contents=error_msg)
        db_manager.update_status(run_id=study_id, status=Status.ERROR)

    def remove_input_dir(self, directory):
        """
        Delete the folder that includes Qiime2 input files.
        """
        try:
            utils.remove_dir(directory)
        except Exception:
            # Leave the folder as is if another process is using it.
            pass

    def send_email(self, recipient, run_id):
        """
        Send an email to the client indicating the given run ID has been processed.
        """
        sender = "Microbiome Platform <microbiome.platform@gmail.com>"
        aws_region = "us-west-2"
        subject = "Process Completed"

        # Email body for non-HTML email clients.
        body_text = f'{run_id} has been processed successfully.'

        # The HTML body of the email.
        body_html = f"""<html>
        <head></head>
        <body>
          <p>{run_id} has been processed successfully.</p>
        </body>
        </html>
                    """

        charset = "UTF-8"

        client = boto3.client('ses', region_name=aws_region)

        # Try to send the email.
        try:
            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        recipient,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': charset,
                            'Data': body_html,
                        },
                        'Text': {
                            'Charset': charset,
                            'Data': body_text,
                        },
                    },
                    'Subject': {
                        'Charset': charset,
                        'Data': subject,
                    },
                },
                Source=sender,
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            self.logger.debug(f"{run_id} | {e.response['Error']['Message']}")
            print(e.response['Error']['Message'])
        else:
            self.logger.debug(f'{run_id} | Email sent to {recipient} successfully.')


