import os
from unittest.mock import Mock

import pytest

import utils
from database_manager.db_manager import db_manager
from study.study import InvalidStudyError, Study


def test_invalid_parent_dir():
    study = Study(parent_dir='', user_id='', is_public='')
    with pytest.raises(InvalidStudyError):
        study.setup()

def test_missing_fastq_files():
    study = Study(parent_dir=os.getcwd(), user_id='', is_public='')
    db_manager.get_layout = Mock(return_value='single')
    with pytest.raises(InvalidStudyError):
        study.setup()

def test_invalid_paired_fastq_file_names():
    study = Study(parent_dir=os.getcwd(), user_id='', is_public='')
    db_manager.get_layout = Mock(return_value='paired')
    utils.get_file_paths = Mock(return_value=['fileNameWithNoUnderscores'])
    with pytest.raises(InvalidStudyError):
        study.setup()




