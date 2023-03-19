from enum import Enum


class InputFormat(str, Enum):
    """
    Represents the format of the data to be imported into Qiime2.
    """

    SINGLE_PHRED_33 = 'SingleEndFastqManifestPhred33V2'
    PAIRED_PHRED_33 = 'PairedEndFastqManifestPhred33V2'
    SINGLE_PHRED_64 = 'SingleEndFastqManifestPhred64V2'
    PAIRED_PHRED_64 = 'PairedEndFastqManifestPhred64V2'