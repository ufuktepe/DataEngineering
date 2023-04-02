import os

import yaml

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yaml')
CLASSIFIER_FILE_NAME = 'classifier_file_name'
ENV = 'env'
LOGGER_PATH = 'logger_path'
LOGGING_LEVEL = 'logging_level'
POST_PROCESSOR_API_IP = 'post_processor_api_ip'
POST_PROCESSOR_API_PORT = 'post_processor_api_port'
LOGGING_LEVELS = {'CRITICAL': 50, 'ERROR': 40, 'WARNING': 30, 'INFO': 20, 'DEBUG': 10, 'NOTSET': 0}
CONFIG_KEYS = {CLASSIFIER_FILE_NAME, ENV, LOGGER_PATH, LOGGING_LEVEL, POST_PROCESSOR_API_IP, POST_PROCESSOR_API_PORT}


class Config:
    """
    Represents the configuration for the Data Engineering module.
    """
    def __init__(self):
        self.config = {}

    def setup(self):
        """
        Load the configuration file and populate the config dictionary.
        """
        if not os.path.exists(CONFIG_PATH):
            raise FileExistsError(f'{CONFIG_PATH} does not exist!')

        with open(CONFIG_PATH, 'r') as yaml_file:
            config_data = yaml.safe_load(yaml_file)
            if not config_data:
                raise ValueError(f'Configuration file error!')
            self.config = config_data[0]

        self.validate()

    def validate(self):
        for key in self.config.keys():
            if key not in CONFIG_KEYS:
                raise ValueError(f'Configuration file error! Invalid key: {key}')

        # Validate the logging level
        level = self.config[LOGGING_LEVEL].upper()
        if level not in LOGGING_LEVELS:
            raise ValueError(f'Configuration file error! Invalid logging level: {level}')

    @property
    def classifier_path(self):
        if CLASSIFIER_FILE_NAME not in self.config:
            return None
        return os.path.join(os.path.dirname(__file__), 'static', self.config[CLASSIFIER_FILE_NAME])

    @property
    def env(self):
        return self.config.get(ENV, None)

    @property
    def logger_path(self):
        return self.config.get(LOGGER_PATH, None)

    @property
    def logging_level(self):
        if LOGGING_LEVEL not in self.config:
            return None
        level = self.config[LOGGING_LEVEL].upper()
        return LOGGING_LEVELS.get(level, None)

    @property
    def post_processing_api_ip(self):
        return self.config.get(POST_PROCESSOR_API_IP, None)

    @property
    def post_processing_api_port(self):
        return self.config.get(POST_PROCESSOR_API_PORT, None)


# Singleton
config = Config()