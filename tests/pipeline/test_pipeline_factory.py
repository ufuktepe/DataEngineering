import os
from unittest.mock import Mock

import pytest

from ...config import config
from ...pipeline.demux_paired_pipeline import DemuxPairedPipeline
from ...pipeline.demux_single_pipeline import DemuxSinglePipeline
from ...pipeline.pipeline_factory import PipelineFactory
from ...static.layout import Layout
from ...study.study import InvalidStudyError, Study


@pytest.fixture(scope="session", autouse=True)
def configure():
    config.setup()

def test_study_with_invalid_layout():
    Study.layout = Mock(return_value=None)
    with pytest.raises(InvalidStudyError):
        PipelineFactory.generate_pipeline(study=Study, logger_name="")

def test_demux_study_with_single_layout():
    study = Study(os.getcwd())
    study.layout = Layout.SINGLE
    pipeline = PipelineFactory.generate_pipeline(study=study, logger_name="")
    assert isinstance(pipeline, DemuxSinglePipeline)

def test_demux_study_with_paired_layout():
    study = Study(os.getcwd())
    study.layout = Layout.PAIRED
    pipeline = PipelineFactory.generate_pipeline(study=study, logger_name="")
    assert isinstance(pipeline, DemuxPairedPipeline)
