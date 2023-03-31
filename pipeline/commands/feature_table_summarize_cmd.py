from pipeline.commands.command import Command


class FeatureTableSummarizeCmd(Command):
    """
    Represents a command to generate visual and tabular summaries of a feature table.
    """

    def __init__(self, input_path, output_path, msg=''):
        super().__init__(msg)
        self.input_path = input_path      # Path to the feature table to be summarized.
        self.output_path = output_path    # Path where output artifact (visualization) should be written.

    def __str__(self):
        return f"qiime feature-table summarize \
               --i-table {self.input_path} \
               --o-visualization {self.output_path}"