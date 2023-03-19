from enum import Enum


class SemanticType(str, Enum):
    """
    Represents a semantic type for a Qiime2 artifact.
    """

    SD_PAIRED_QUALITY = 'SampleData[PairedEndSequencesWithQuality]'
    SD_SINGLE_QUALITY = 'SampleData[SequencesWithQuality]'