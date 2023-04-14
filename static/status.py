from enum import IntEnum


class Status(IntEnum):
    """
    Represents the run status.
    """

    RECEIVED_REQUEST = 0
    PROCESSING = 1
    SUCCESS = 2
    ERROR = 3