class DBError(Exception):
    """
    Exception to indicate a database error.
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f'{self.msg}'
