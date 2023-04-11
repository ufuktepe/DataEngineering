#!/usr/bin/env python

import json
import os
import sys
import time

import psycopg2
import requests

import utils
from config import config
from pipeline.pipeline_error import PipelineError
from pipeline.pipeline_factory import PipelineFactory
from static import constants as const
from study.study import InvalidStudyError
from study.study import Study

LOGGER_NAME = 'data_engineering'


class DataEngineering:
    """
    Represents the Data Engineering Module.
    """
    def __init__(self):
        self.logger = None

    def setup(self):
        """
        Set up the configuration and logger.
        """
        try:
            config.setup()
        except FileExistsError as e:
            raise ValueError(e)

        self.logger = utils.setup_logger(logger_name=LOGGER_NAME, logging_level=config.logging_level)

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

        # Validate the directory.
        if not os.path.isdir(directory):
            print('Please provide a valid directory.')
            return

        print(f'Monitoring {directory}')
        while True:
            time.sleep(3)
            for root, sub_dirs, file_names in os.walk(directory):
                if Study.is_ready_for_processing(file_names):
                    self.process_study(root)

    def process_study(self, directory):
        """
        Create a study from the user provided directory. Then create a Qiime2 pipeline and execute it.
        """
        start_time = time.time()

        self.logger.debug(f'Processing {os.path.basename(directory)}')
        study = Study(directory)
        try:
            study.setup()
        except InvalidStudyError as e:
            self.logger.critical(e)
            utils.create_txt(file_path=os.path.join(directory, const.ERROR_MARKER), contents=e)
            return

        self.logger.debug(f'{study.id} | Generating a Qiime2 pipeline.')
        try:
            pipeline = PipelineFactory.generate_pipeline(study, LOGGER_NAME)
        except InvalidStudyError as e:
            self.logger.critical(e)
            utils.create_txt(file_path=os.path.join(directory, const.ERROR_MARKER), contents=e)
            return

        self.logger.debug(f'{study.id} | Executing the pipeline.')
        try:
            pipeline.execute()
        except PipelineError as e:
            self.logger.error(f'{e.study_id} | {e.msg}')
            utils.create_txt(file_path=os.path.join(directory, const.ERROR_MARKER), contents=e)
            return

        self.logger.debug(f'{study.id} | Creating the results csv file.')
        try:
            utils.create_results_csv(feature_table_path=pipeline.get_feature_table_path(),
                                     taxonomy_results_path=pipeline.get_taxonomy_results_path(),
                                     output_dir=pipeline.get_output_dir())
        except ValueError as e:
            self.logger.error(f'{study.id} | {str(e)}')
            utils.create_txt(file_path=os.path.join(directory, const.ERROR_MARKER), contents=e)
            return

        utils.create_txt(file_path=os.path.join(directory, const.PROCESSED_MARKER))

        # Post the results
        if self.post_study(study) == 201:
            self.logger.info(f'{study.id} | Sent results to Post Processing API successfully.')
        else:
            self.logger.warning(f'{study.id} | Error sending the results to Post Processing API.')

        self.logger.info(f'{study.id} | Process Completed. Runtime: {utils.get_runtime(start_time)}')


    def post_results(self, results_csv):
        """
        Send the results to the database.
        """
        conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")
        cur = conn.cursor()
        with open(results_csv, 'r') as f:
            next(f)  # Skip the header row.
            cur.copy_from(f, 'users', sep=',')

        conn.commit()



        # studies = [{'id': study.id,
        #             'library_layout': study.layout,
        #             'feature_table_path': os.path.join(study.parent_dir, 'output', f'{study.id}_feature-table.qza'),
        #             'taxonomy_results_path': os.path.join(study.parent_dir, 'output', f'{study.id}_taxonomy.qza')}
        #            ]
        #
        # # Send a POST request to the Post Processor API.
        # response = requests.post(f'http://{config.post_processing_api_ip}:{config.post_processing_api_port}/',
        #                          data=json.dumps(studies))
        #
        # return response.status_code


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