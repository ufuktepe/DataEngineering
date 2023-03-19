from pipeline.commands.import_cmd import ImportCmd
from pipeline.commands.single_denoise_cmd import SingleDenoiseCmd
from pipeline.pipeline import Pipeline
from static.input_format import InputFormat
from static.semantic_type import SemanticType


class DemuxSinglePipeline(Pipeline):
    """
    Pipeline for a demultiplexed study that includes single-end reads.
    """

    def __init__(self, study):
        super().__init__(study)
        self.setup_unique_commands()
        self.setup_common_commands()

    def setup_unique_commands(self):
        """
        Generate unique commands for this pipeline and add them to the commands list.
        """
        self.commands.append(ImportCmd(input_type=SemanticType.SD_SINGLE_QUALITY,
                                       input_path=self.manifest_path,
                                       output_path=self.demux_path,
                                       input_format=InputFormat.SINGLE_PHRED_33,
                                       msg='Importing into Qiime2...'))

        self.commands.append(SingleDenoiseCmd(input_path=self.demux_path,
                                              trunc_pos=0,
                                              output_path=self.qza_table_path,
                                              rep_seqs_path=self.rep_seqs_path,
                                              stats_path=self.stats_path,
                                              msg='Running DADA2...'))