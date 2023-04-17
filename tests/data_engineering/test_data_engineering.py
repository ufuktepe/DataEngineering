import pytest

import config
from data_engineering import DataEngineering


def test_missing_config_file():
    data_engineering = DataEngineering()
    config.CONFIG_PATH = ''
    with pytest.raises(ValueError):
        data_engineering.setup()


def test_invalid_input_directory():
    data_engineering = DataEngineering()
    config.app_config.attributes['input_path'] = None
    with pytest.raises(ValueError):
        data_engineering.run()