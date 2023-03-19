class InvalidStudyError(Exception):
    """
    Exception to indicate an invalid study.
    """

    def __init__(self, msg, parent_dir):
        self.msg = msg
        self.parent_dir = parent_dir

    def __str__(self):
        return f'{self.msg}\nStudy Dir: {self.parent_dir}'
