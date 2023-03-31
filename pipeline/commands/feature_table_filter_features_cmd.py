from pipeline.commands.command import Command


class FeatureTableFilterFeaturesCmd(Command):
    """
    Represents a command to filter features from table based on frequency and/or metadata. Any samples with a
    frequency of zero after feature filtering will also be removed.
    """

    def __init__(self, qza_table_path, feature_metadata, output_path, msg=''):
        super().__init__(msg)
        self.qza_table_path = qza_table_path      # Path to the feature table from which features should be filtered.
        self.feature_metadata = feature_metadata  # Feature metadata. All features in feature metadata that are also in
                                                  # the feature table will be retained.
        self.output_path = output_path            # Path where output artifact should be written.


    def __str__(self):
        return f"qiime feature-table filter-features \
               --i-table {self.qza_table_path} \
               --m-metadata-file {self.feature_metadata} \
               --o-filtered-table {self.output_path}"