import os

import pytest

from config import config
from study import Study, InvalidStudyError


@pytest.fixture(scope="session", autouse=True)
def configure():
    config.setup()

@pytest.fixture
def study():
    return Study(os.getcwd())

def test_invalid_parent_dir():
    study = Study("")
    with pytest.raises(InvalidStudyError):
        study.setup()

def test_missing_metadata():
    study = Study(os.getcwd())
    with pytest.raises(InvalidStudyError):
        study.setup()




