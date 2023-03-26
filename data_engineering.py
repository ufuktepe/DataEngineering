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
        Create a study from the user provided directory. Then create a Qiime2 pipeline and execute it.
        """
        start_time = time.time()

        # # Check arguments.
        # if len(sys.argv) != 2:
        #     print('Please provide an input directory.')
        #     return
        #
        # # Get the local directory.
        # local_dir = sys.argv[1]

        local_dir = r'/Users/burak/Qiime2/SRA_Toolkit_Trials/temp'

        self.logger.info('Generating a study.')
        study = Study(local_dir)
        try:
            study.setup()
        except InvalidStudyError as e:
            self.logger.critical(e)
            return

        self.logger.info('Generating a Qiime2 pipeline.')
        try:
            pipeline = PipelineFactory.generate_pipeline(study)
        except InvalidStudyError as e:
            self.logger.critical(e)
            return

        self.logger.info('Executing the pipeline.')
        pipeline.execute()

        self.logger.info(f'Process Completed. Runtime: {utils.get_runtime(start_time)}')

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