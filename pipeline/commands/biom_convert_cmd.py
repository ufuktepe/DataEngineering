from .command import Command


class BiomConvertCmd(Command):
    """
    Represents a command to convert from the biom format.
    """

    def __init__(self, input_path, output_path, output_format, msg=''):
        super().__init__(msg)
        self.input_path = input_path        # Path for the input biom file.
        self.output_path = output_path      # Path for the output file.
        self.output_format = output_format  # Output file format (json, hdf5, or tsv).

    def __str__(self):
        return f"biom convert \
               -i {self.input_path} \
               -o {self.output_path} \
               --to-{self.output_format}"