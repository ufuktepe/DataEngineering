import os

import pytest

# from study import Study, InvalidStudyError
from study.study import Study
from study.invalid_study_error import InvalidStudyError

@pytest.fixture
def study():
    return Study(os.getcwd())

def test_invalid_parent_dir():
    study = Study("")
    with pytest.raises(InvalidStudyError):
        study.setup()




