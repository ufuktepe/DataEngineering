from .commands.import_cmd import ImportCmd
from .commands.paired_denoise_cmd import PairedDenoiseCmd
from .pipeline import Pipeline
from ..static.input_format import InputFormat
from ..static.semantic_type import SemanticType


class DemuxPairedPipeline(Pipeline):
    """
    Pipeline for a demultiplexed study that includes paired-end reads.
    """

    def __init__(self, study, logger_name):
        super().__init__(study, logger_name)
        self.setup_unique_commands()
        self.setup_common_commands()

    def setup_unique_commands(self):
        """
        Generate unique commands for this pipeline and add them to the commands list.
        """
        self.commands.append(ImportCmd(input_type=SemanticType.SD_PAIRED_QUALITY,
                                       input_path=self.manifest_path,
                                       output_path=self.demux_path,
                                       input_format=InputFormat.PAIRED_PHRED_33,
                                       msg=f'{self.id} | Importing into Qiime2.'))

        self.commands.append(PairedDenoiseCmd(input_path=self.demux_path,
                                              fwd_trunc_pos=0,
                                              rev_trunc_pos=0,
                                              output_path=self.qza_table_path,
                                              rep_seqs_path=self.rep_seqs_path,
                                              stats_path=self.stats_path,
                                              msg=f'{self.id} | Running DADA2.'))