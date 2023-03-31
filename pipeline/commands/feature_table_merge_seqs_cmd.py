from pipeline.commands.command import Command


class FeatureTableMergeSeqsCmd(Command):
    """
    Represents a command to combine feature data objects.
    """

    def __init__(self, input_path, output_path, msg=''):
        super().__init__(msg)
        self.input_path = input_path      # Path to feature sequences to be merged separated by spaces.
        self.output_path = output_path    # Path where output artifact should be written.

    def __str__(self):
        return f"qiime feature-table merge-seqs \
               --i-data {self.input_path} \
               --o-merged-data {self.output_path}"