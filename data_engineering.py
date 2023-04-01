#!/usr/bin/env python

import os
import sys
import time

from config import config
from pipeline import PipelineFactory
from pipeline.pipeline_error import PipelineError
from static import constants as const
from study import InvalidStudyError
from study import Study
import utils


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
            pipeline = PipelineFactory.generate_pipeline(study)
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

        self.logger.info(f'{study.id} | Process Completed. Runtime: {utils.get_runtime(start_time)}')
        utils.create_empty_txt(file_path=os.path.join(directory, const.PROCESSED_MARKER))


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