import os
from unittest.mock import Mock

import pytest

import utils
from config import app_config
from pipeline.pipeline_error import PipelineError
from pipeline.pipeline_factory import PipelineFactory
from static.layout import Layout
from study.study import Study


def test_study_with_no_id():
    study = Study(parent_dir=os.getcwd(), user_id='', is_public='')
    study.layout = Layout.SINGLE
    study.id = None
    with pytest.raises(PipelineError):
        PipelineFactory.generate_pipeline(study=study, logger_name="")


def test_missing_private_results_path():
    study = Study(parent_dir=os.getcwd(), user_id='dummy', is_public=False)
    study.layout = Layout.PAIRED
    app_config.attributes['private_results_path'] = None
    with pytest.raises(PipelineError):
        PipelineFactory.generate_pipeline(study=study, logger_name="")


def test_missing_public_results_path():
    study = Study(parent_dir=os.getcwd(), user_id=None, is_public=True)
    study.layout = Layout.PAIRED
    app_config.attributes['public_results_path'] = None
    with pytest.raises(PipelineError):
        PipelineFactory.generate_pipeline(study=study, logger_name="")


def test_qiime_error():
    utils.run_conda_command = Mock(return_value=1)
    study = Study(parent_dir=os.getcwd(), user_id=None, is_public=True)
    study.layout = Layout.SINGLE
    study.id = 'dummy'
    app_config.attributes['public_results_path'] = 'dummy'
    pipeline = PipelineFactory.generate_pipeline(study=study, logger_name="")
    with pytest.raises(PipelineError):
        pipeline.execute()

    # Clean up
    utils.remove_dir(os.path.join(os.getcwd(), 'dummy'))
