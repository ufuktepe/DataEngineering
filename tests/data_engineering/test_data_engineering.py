import pytest

from config import *
from data_engineering import DataEngineering


def test_missing_config_file():
    data_engineering = DataEngineering()
    with pytest.raises(ValueError):
        data_engineering.setup(config_file_name=None)


def test_invalid_input_directory():
    data_engineering = DataEngineering()
    app_config.attributes['input_path'] = None
    with pytest.raises(ValueError):
        data_engineering.run()