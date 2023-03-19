from abc import ABC


class Command(ABC):
    """
    Abstract class representing a Qiime2 command.
    """

    def __init__(self, msg):
        self.msg = msg  # Message to be displayed before executing the command.

    def get_msg(self):
        return self.msg

