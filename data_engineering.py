import os
import sys
import time

from config import config
from pipeline import PipelineFactory
from study import Study
from study import InvalidStudyError
import utils


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

        self.logger = utils.setup_logger(config.logger_name, config.logger_path)

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

        while True:
            for root, sub_dirs, file_names in os.walk(directory):
                if utils.is_study_ready(file_names):
                    self.process_study(root)

    def process_study(self, directory):
        """
        Create a study from the user provided directory. Then create a Qiime2 pipeline and execute it.
        """
        start_time = time.time()

        self.logger.info(f'Processing {os.path.basename(directory)}')
        study = Study(directory)
        try:
            study.setup()
        except InvalidStudyError as e:
            self.logger.critical(e)
            return

        self.logger.info(f'{study.id} | Generating a Qiime2 pipeline.')
        try:
            pipeline = PipelineFactory.generate_pipeline(study)
        except InvalidStudyError as e:
            self.logger.critical(e)
            return

        self.logger.info(f'{study.id} | Executing the pipeline.')
        pipeline.execute()

        self.logger.info(f'{study.id} | Process Completed. Runtime: {utils.get_runtime(start_time)}')

        with open(os.path.join(directory, 'processed.txt'), 'w') as _:
            pass


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