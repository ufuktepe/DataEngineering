import os
import yaml


CONFIG_PATH = './config.yaml'
CLASSIFIER_PATH = 'classifier_path'
ENV = 'env'
LOGGER_NAME = 'logger_name'
LOGGER_PATH = 'logger_path'
META_DATA_EXT = 'meta_data_ext'
LAYOUT_TITLE = 'layout_title'
CONFIG_KEYS = {CLASSIFIER_PATH, ENV, LOGGER_NAME, LOGGER_PATH, META_DATA_EXT, LAYOUT_TITLE}


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
        if CLASSIFIER_PATH not in self.config:
            return None
        return self.config[CLASSIFIER_PATH]

    @property
    def env(self):
        if ENV not in self.config:
            return None
        return self.config[ENV]

    @property
    def logger_name(self):
        if LOGGER_NAME not in self.config:
            return None
        return self.config[LOGGER_NAME]

    @property
    def logger_path(self):
        if LOGGER_PATH not in self.config:
            return None
        return self.config[LOGGER_PATH]

    @property
    def meta_data_ext(self):
        if META_DATA_EXT not in self.config:
            return None
        return self.config[META_DATA_EXT]

    @property
    def layout_title(self):
        if LAYOUT_TITLE not in self.config:
            return None
        return self.config[LAYOUT_TITLE]

config = Config()