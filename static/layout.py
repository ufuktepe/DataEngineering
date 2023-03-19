from enum import Enum


class Layout(str, Enum):
    """
    Represents the type of sequencing layout.
    """

    SINGLE = 'single'
    PAIRED = 'paired'