import os

import yaml

CLASSIFIER_FILE_NAME = 'classifier_file_name'
ENV = 'env'
CONDA_PATH = 'conda_path'
INPUT_PATH = 'input_path'
PRIVATE_RESULTS_PATH = 'private_results_path'
PUBLIC_RESULTS_PATH = 'public_results_path'
AWS_ACCESS_KEY_ID = 'aws_access_key_id'
AWS_SECRET_ACCESS_KEY = 'aws_secret_access_key'
LOGGING_LEVEL = 'logging_level'
DB_HOST = 'db_host'
DB_PORT = 'db_port'
DB_USERNAME = 'db_username'
DB_PASSWORD = 'db_password'
DB_NAME = 'db_name'
DB_TABLE_METADATA = 'db_table_metadata'
DB_TABLE_RESULTS = 'db_table_results'
DB_TABLE_STATUS = 'db_table_status'
LOGGING_LEVELS = {'CRITICAL': 50, 'ERROR': 40, 'WARNING': 30, 'INFO': 20, 'DEBUG': 10, 'NOTSET': 0}
CONFIG_KEYS = {CLASSIFIER_FILE_NAME, ENV, CONDA_PATH, INPUT_PATH, PRIVATE_RESULTS_PATH, PUBLIC_RESULTS_PATH,
               AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, LOGGING_LEVEL, DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD,
               DB_NAME, DB_TABLE_METADATA, DB_TABLE_RESULTS, DB_TABLE_STATUS}


class Config:
    """
    Represents the configuration for the Data Engineering module.
    """
    def __init__(self):
        self.attributes = {}

    def setup(self, config_file_name):
        """
        Load the configuration file and populate the config dictionary.
        """
        if not isinstance(config_file_name, str) or not len(config_file_name):
            raise ValueError(f'Invalid configuration file name!')

        config_file_path = os.path.join(os.path.dirname(__file__), config_file_name)

        if not os.path.exists(config_file_path):
            raise FileExistsError(f'{config_file_path} does not exist!')

        with open(config_file_path, 'r') as yaml_file:
            config_data = yaml.safe_load(yaml_file)
            if not config_data:
                raise ValueError(f'Configuration file error!')
            self.attributes = config_data[0]

        self.validate()

        # Set environment variables
        os.environ['AWS_ACCESS_KEY_ID'] = app_config.aws_access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] = app_config.aws_secret_access_key

    def validate(self):
        for key in self.attributes.keys():
            if key not in CONFIG_KEYS:
                raise ValueError(f'Configuration file error! Invalid key: {key}')

        # Validate the logging level
        level = self.attributes[LOGGING_LEVEL].upper()
        if level not in LOGGING_LEVELS:
            raise ValueError(f'Configuration file error! Invalid logging level: {level}')

    @property
    def classifier_path(self):
        if CLASSIFIER_FILE_NAME not in self.attributes:
            return None
        return os.path.join(os.path.dirname(__file__), 'static', self.attributes[CLASSIFIER_FILE_NAME])

    @property
    def env(self):
        return self.attributes.get(ENV, None)

    @property
    def conda_path(self):
        return self.attributes.get(CONDA_PATH, None)

    @property
    def input_path(self):
        return self.attributes.get(INPUT_PATH, None)

    @property
    def private_results_path(self):
        return self.attributes.get(PRIVATE_RESULTS_PATH, None)

    @property
    def public_results_path(self):
        return self.attributes.get(PUBLIC_RESULTS_PATH, None)

    @property
    def aws_access_key_id(self):
        return self.attributes.get(AWS_ACCESS_KEY_ID, None)

    @property
    def aws_secret_access_key(self):
        return self.attributes.get(AWS_SECRET_ACCESS_KEY, None)

    @property
    def logging_level(self):
        if LOGGING_LEVEL not in self.attributes:
            return None
        level = self.attributes[LOGGING_LEVEL].upper()
        return LOGGING_LEVELS.get(level, None)

    @property
    def db_host(self):
        return self.attributes.get(DB_HOST, None)

    @property
    def db_port(self):
        return self.attributes.get(DB_PORT, None)

    @property
    def db_username(self):
        return self.attributes.get(DB_USERNAME, None)

    @property
    def db_password(self):
        return self.attributes.get(DB_PASSWORD, None)

    @property
    def db_name(self):
        return self.attributes.get(DB_NAME, None)

    @property
    def db_table_metadata(self):
        return self.attributes.get(DB_TABLE_METADATA, None)

    @property
    def db_table_results(self):
        return self.attributes.get(DB_TABLE_RESULTS, None)

    @property
    def db_table_status(self):
        return self.attributes.get(DB_TABLE_STATUS, None)


# Singleton
app_config = Config()