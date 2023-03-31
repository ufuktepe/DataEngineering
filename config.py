import os

import yaml

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yaml')
CLASSIFIER_FILE_NAME = 'classifier_file_name'
ENV = 'env'
LOGGER_PATH = 'logger_path'
CONFIG_KEYS = {CLASSIFIER_FILE_NAME, ENV, LOGGER_PATH}


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
                raise ValueError('Invalid configuration file!')
            self.config = config_data[0]

        self.validate()

    def validate(self):
        for key in self.config.keys():
            if key not in CONFIG_KEYS:
                raise ValueError('Invalid configuration file!')

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


# Singleton
config = Config()