from .command import Command


class ImportCmd(Command):
    """
    Represents a command to import data to create a new Qiime2 artifact.
    """

    def __init__(self, input_type, input_path, output_path, input_format, msg=''):
        super().__init__(msg)
        self.input_type = input_type      # The semantic type of the artifact that will be created upon importing.
        self.input_path = input_path      # Path to file or directory that should be imported.
        self.output_path = output_path    # Path where output artifact should be written.
        self.input_format = input_format  # The format of the data to be imported.

    def __str__(self):
        return f"qiime tools import \
               --type '{self.input_type}' \
               --input-path {self.input_path} \
               --output-path {self.output_path} \
               --input-format {self.input_format}"
