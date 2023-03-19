from static.layout import Layout
from pipeline.demux_single_pipeline import DemuxSinglePipeline
from pipeline.demux_paired_pipeline import DemuxPairedPipeline
from study.study import InvalidStudyError


PIPELINES = {Layout.SINGLE: DemuxSinglePipeline,
             Layout.PAIRED: DemuxPairedPipeline}


class PipelineFactory:
    """
    Factory class to generate pipelines.
    """

    @classmethod
    def generate_pipeline(cls, study):
        """
        Return a pipeline based on the given study. Raise an InvalidStudyError if the type of the study cannot be
        identified.
        """
        try:
            return PIPELINES[study.get_layout()](study)
        except KeyError:
            raise InvalidStudyError('Unsupported study type!')