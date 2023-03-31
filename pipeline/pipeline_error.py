class PipelineError(Exception):
    """
    Exception to indicate an error in pipeline.
    """

    def __init__(self, msg, study_id):
        self.msg = msg
        self.study_id = study_id

    def __str__(self):
        return f'{self.study_id} | {self.msg}'
