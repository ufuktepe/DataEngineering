#!/usr/bin/env python

import json
import os
import sys
import time

import psycopg2
import requests

import utils
from config import config
from database_manager.db_error import DBError
from database_manager.db_manager import db_manager
from pipeline.pipeline_error import PipelineError
from pipeline.pipeline_factory import PipelineFactory
from static import constants as const
from study.study import InvalidStudyError
from study.study import Study
from static.status import Status

LOGGER_NAME = 'data_engineering'


class DataEngineering:
    """
    Represents the Data Engineering Module.
    """
    def __init__(self):
        self.logger = None

    def setup(self):
        """
        Set up the configuration, logger, and db manager.
        """
        try:
            config.setup()
        except FileExistsError as e:
            raise ValueError(e)

        self.logger = utils.setup_logger(logger_name=LOGGER_NAME, logging_level=config.logging_level)

        try:
            db_manager.setup(config)
        except DBError as e:
            raise ValueError(e)

    def run(self):
        """
        Constantly crawl the given directory to find downloaded studies. Process all studies that are ready to be
        processed.
        """
        # Check arguments.
        if len(sys.argv) != 2:
            print('Please provide an input directory.')
            return

        # Get the directory.
        directory = sys.argv[1]
        # directory = '/Volumes/Burak_HDD/qiime2/small_subset_test'

        # Validate the directory.
        if not os.path.isdir(directory):
            print('Please provide a valid directory.')
            return

        print(f'Monitoring {directory}')
        while True:
            time.sleep(3)
            for root, sub_dirs, file_names in os.walk(directory):
                if Study.is_ready_for_processing(file_names):
                    # Claim the study
                    try:
                        utils.create_txt(file_path=os.path.join(root, const.CLAIMED_MARKER))
                    except ValueError:
                        continue

                    # Process the study
                    self.process_study(root)

    def process_study(self, directory):
        """
        Create a study from the user provided directory. Then create a Qiime2 pipeline and execute it.
        """
        # Check if the claimed marker belongs to this process
        if not utils.is_file_owned_by_me(file_path=os.path.join(directory, const.CLAIMED_MARKER)):
            return

        start_time = time.time()

        study_id = os.path.basename(directory)

        db_manager.update_status(run_id=study_id, status=Status.PROCESSING)

        self.logger.debug(f'Processing {study_id}')
        study = Study(directory)
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
            results_csv_path = utils.create_results_csv(feature_table_path=pipeline.get_feature_table_path(),
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
        db_manager.update_status(run_id=study_id, status=Status.SUCCESS)

    def error_out(self, study_id, error_msg, directory):
        """
        Log the error message, create an error text file, and update the status table.
        """
        self.logger.error(f'{study_id} | {error_msg}')
        utils.create_txt(file_path=os.path.join(directory, const.ERROR_MARKER), contents=error_msg)
        db_manager.update_status(run_id=study_id, status=Status.ERROR)


def main():
    data_engineering = DataEngineering()

    try:
        data_engineering.setup()
    except ValueError as e:
        print(e)
        return

    data_engineering.run()


if __name__ == '__main__':
    main()