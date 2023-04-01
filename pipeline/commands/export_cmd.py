from .command import Command


class ExportCmd(Command):
    """
    Represents a command to export data from a Qiime2 artifact.
    """

    def __init__(self, input_path, output_path, msg=''):
        super().__init__(msg)
        self.input_path = input_path    # Path to file that should be exported.
        self.output_path = output_path  # Path to file or directory where data should be exported to.

    def __str__(self):
        return f"qiime tools export \
               --input-path {self.input_path} \
               --output-path {self.output_path}"