#!/usr/bin/env python

import json
import os
import sys
import time

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
            utils.create_empty_txt(file_path=os.path.join(directory, const.ERROR_MARKER))
            return

        self.logger.debug(f'{study.id} | Generating a Qiime2 pipeline.')
        try:
            pipeline = PipelineFactory.generate_pipeline(study, LOGGER_NAME)
        except InvalidStudyError as e:
            self.logger.critical(e)
            utils.create_empty_txt(file_path=os.path.join(directory, const.ERROR_MARKER))
            return

        self.logger.debug(f'{study.id} | Executing the pipeline.')
        try:
            pipeline.execute()
        except PipelineError as e:
            self.logger.error(f'{e.study_id} | {e.msg}')
            utils.create_empty_txt(file_path=os.path.join(directory, const.ERROR_MARKER))
            return

        # Post the results
        if self.post_study(study) == 201:
            self.logger.info(f'{study.id} | Sent results to Post Processing API successfully.')
        else:
            self.logger.warning(f'{study.id} | Error sendig the results to Post Processing API.')

        self.logger.info(f'{study.id} | Process Completed. Runtime: {utils.get_runtime(start_time)}')
        utils.create_empty_txt(file_path=os.path.join(directory, const.PROCESSED_MARKER))

    def post_study(self, study):
        """
        Post the study to the Post Processing API.
        """
        studies = [{'id': study.id,
                    'library_layout': study.layout,
                    'feature_table_path': os.path.join(study.parent_dir, 'output', f'{study.id}_feature-table.qza'),
                    'taxonomy_results_path': os.path.join(study.parent_dir, 'output', f'{study.id}_taxonomy.qza')}
                   ]

        response = requests.post(f'http://{config.post_processing_api_ip}:{config.post_processing_api_port}/',
                                 data=json.dumps(studies))

        return response.status_code



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