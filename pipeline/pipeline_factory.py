from .demux_paired_pipeline import DemuxPairedPipeline
from .demux_single_pipeline import DemuxSinglePipeline
from static.layout import Layout
from study.study import InvalidStudyError

PIPELINES = {Layout.SINGLE: DemuxSinglePipeline,
             Layout.PAIRED: DemuxPairedPipeline}


class PipelineFactory:
    """
    Factory class to generate pipelines.
    """

    @classmethod
    def generate_pipeline(cls, study, logger_name):
        """
        Return a pipeline based on the given study. Raise an InvalidStudyError if the type of the study cannot be
        identified.
        """
        try:
            return PIPELINES[study.layout](study, logger_name)
        except KeyError:
            raise InvalidStudyError(msg='Unsupported study type!', study_id='N/A')