from pipeline.commands.command import Command


class FeatureTableMergeCmd(Command):
    """
    Represents a command to combine feature tables.
    """

    def __init__(self, input_path, output_path, overlap_method='sum', msg=''):
        super().__init__(msg)
        self.input_path = input_path          # Path to feature tables to be merged separated by spaces.
        self.output_path = output_path        # Path where output artifact should be written.
        self.overlap_method = overlap_method  # Method for handling overlapping ids. overlap methods are 'average',
                                              # 'error_on_overlapping_feature', 'error_on_overlapping_sample', 'sum'

    def __str__(self):
        return f"qiime feature-table merge \
               --i-tables {self.input_path} \
               --o-merged-table {self.output_path}"