from pipeline.commands.command import Command


class MetadataTabulateCmd(Command):
    """
    Represents a command to generate a tabular view of Metadata. Used to convert taxonomy analysis results from qza
    to qzv.
    """

    def __init__(self, input_path, output_path, msg=''):
        super().__init__(msg)
        self.input_path = input_path      # Path to the metadata (taxonomy analysis results) to be tabulated.
        self.output_path = output_path    # Path where output artifact (visualization) should be written.

    def __str__(self):
        return f"qiime metadata tabulate \
               --m-input-file {self.input_path} \
               --o-visualization {self.output_path}"