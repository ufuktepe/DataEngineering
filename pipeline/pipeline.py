import logging
import os
from abc import ABC

from .commands.biom_convert_cmd import BiomConvertCmd
from .commands.export_cmd import ExportCmd
from .commands.feature_classifier_cmd import FeatureClassifierCmd
from .commands.feature_table_summarize_cmd import FeatureTableSummarizeCmd
from .commands.metadata_tabulate_cmd import MetadataTabulateCmd
from .pipeline_error import PipelineError
import utils
from config import app_config
from static.file_format import FileFormat


class Pipeline(ABC):
    """
    Abstract class for a Qiime2 pipeline.
    """

    def __init__(self, study, logger_name):
        self.logger = logging.getLogger(logger_name)
        
        # ID for the pipeline (same as study ID)
        self.id = study.id

        # Directory for Qiime2 results.
        self.output_dir = self.set_output_dir(study)

        # Path for the manifest file.
        self.manifest_path = study.manifest_path

        # Path for demultiplexed Qiime2 artifact.
        self.demux_path = os.path.join(self.output_dir, f'{study.id}_demux.qza')

        # Path for qza feature table.
        self.qza_table_path = os.path.join(self.output_dir, f'{study.id}_feature-table.qza')

        # Path for qzv feature table.
        self.qzv_table_path = os.path.join(self.output_dir, f'{study.id}_feature-table.qzv')

        # Path for tsv feature table.
        self.tsv_table_path = os.path.join(self.output_dir, f'{study.id}_feature-table.tsv')

        # Path for biom feature table.
        self.biom_table_path = os.path.join(self.output_dir, f'feature-table.biom')

        # Path for representative sequences.
        self.rep_seqs_path = os.path.join(self.output_dir, f'{study.id}_rep_seqs.qza')

        # Path for denoising statistics.
        self.stats_path = os.path.join(self.output_dir, f'{study.id}_stats.qza')

        # Path for qza taxonomy results.
        self.qza_taxonomy_path = os.path.join(self.output_dir, f'{study.id}_taxonomy.qza')

        # Path for qzv taxonomy results.
        self.qzv_taxonomy_path = os.path.join(self.output_dir, f'{study.id}_taxonomy.qzv')

        # List of commands to be executed.
        self.commands = []

    def set_output_dir(self, study):
        """
        Set the output directory for Qiime2 results.
        """
        # Check if study id exists.
        if study.id is None:
            raise PipelineError(msg='Pipeline error: missing study id.', study_id=self.id)

        # Check if study is private
        if study.user_id and not study.is_public:
            if app_config.private_results_path is None:
                raise PipelineError(msg='Pipeline error: missing private results path.', study_id=self.id)

            return os.path.join(app_config.private_results_path, study.user_id, study.id)

        # Check if public results path exists.
        if app_config.public_results_path is None:
            raise PipelineError(msg='Pipeline error: missing public results path.', study_id=self.id)

        # Public study
        return os.path.join(app_config.public_results_path, study.id)

    def get_feature_table_path(self):
        return self.tsv_table_path

    def get_taxonomy_results_path(self):
        return os.path.join(self.output_dir, 'taxonomy.tsv')

    def get_output_dir(self):
        return self.output_dir

    def setup_common_commands(self):
        """
        Populate the commands list with common commands.
        """
        # Command to export a qza feature table in biom format.
        self.commands.append(ExportCmd(input_path=self.qza_table_path,
                                       output_path=self.output_dir,
                                       msg=f'{self.id} | Exporting the Feature Table.'))

        # Command to convert a biom feature table to tsv.
        self.commands.append(BiomConvertCmd(input_path=self.biom_table_path,
                                            output_path=self.tsv_table_path,
                                            output_format=FileFormat.TSV,
                                            msg=f'{self.id} | Converting the Feature Table to tsv.'))

        # Command to generate a qzv feature table.
        # self.commands.append(FeatureTableSummarizeCmd(input_path=self.qza_table_path,
        #                                               output_path=self.qzv_table_path,
        #                                               msg=f'{self.id} | Converting the Feature Table to qzv.'))

        # Command to export representative sequences in fasta format.
        # self.commands.append(ExportCmd(input_path=self.rep_seqs_path,
        #                                output_path=self.output_dir,
        #                                msg=f'{self.id} | Exporting Representative Sequences.'))

        # Command to execute taxonomy analysis.
        self.commands.append(FeatureClassifierCmd(input_path=self.rep_seqs_path,
                                                  classifier_path=app_config.classifier_path,
                                                  output_path=self.qza_taxonomy_path,
                                                  msg=f'{self.id} | Running Taxonomy Analysis.'))

        # Command to export taxonomy analysis results.
        self.commands.append(ExportCmd(input_path=self.qza_taxonomy_path,
                                       output_path=self.output_dir,
                                       msg=f'{self.id} | Exporting Taxonomy Analysis Results.'))

        # Command to generate a qzv for taxonomy results.
        # self.commands.append(MetadataTabulateCmd(input_path=self.qza_taxonomy_path,
        #                                          output_path=self.qzv_taxonomy_path,
        #                                          msg=f'{self.id} | Converting Taxonomy results to qzv.'))

    def execute(self):
        """
        Run the Qiime2 pipeline.
        """
        utils.create_dir(self.output_dir)

        for command in self.commands:
            self.logger.debug(command.get_msg())
            return_code = utils.run_conda_command(cmd=str(command), conda_path=app_config.conda_path, env=app_config.env)
            if return_code != 0:
                raise PipelineError(msg='Pipeline error.', study_id=self.id)

