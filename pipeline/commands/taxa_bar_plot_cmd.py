from pipeline.commands.command import Command


class TaxaBarPlotCmd(Command):
    """
    Represents a command to produce an interactive bar plot visualization of taxonomies.
    """

    def __init__(self, qza_table_path, qza_taxonomy_path, output_path, msg=''):
        super().__init__(msg)
        self.qza_table_path = qza_table_path        # Path to feature table to visualize at various taxonomic levels.
        self.qza_taxonomy_path = qza_taxonomy_path  # Taxonomic annotations for features in the provided feature.
        self.output_path = output_path              # Path where output artifact (visualization) should be written.

    def __str__(self):
        return f"qiime taxa barplot \
               --i-table {self.qza_table_path} \
               --i-taxonomy {self.qza_taxonomy_path} \
               --o-visualization {self.output_path}"