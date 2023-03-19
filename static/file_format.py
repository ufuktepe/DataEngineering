from enum import Enum


class FileFormat(str, Enum):
    """
    Represents a file format for Qiime2.
    """

    TSV = 'tsv'
    HDF5 = 'hdf5'
    JSON = 'json'