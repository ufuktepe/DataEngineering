import os

import pytest

from ...config import config
from ...study.study import Study, InvalidStudyError


@pytest.fixture(scope="session", autouse=True)
def configure():
    config.setup()

def test_invalid_parent_dir():
    study = Study("")
    with pytest.raises(InvalidStudyError):
        study.setup()

def test_missing_metadata():
    study = Study(os.getcwd())
    with pytest.raises(InvalidStudyError):
        study.setup()




