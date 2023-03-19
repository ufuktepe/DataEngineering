from pipeline.commands.command import Command


class PairedDenoiseCmd(Command):
    """
    Represents a command to denoise paired-end sequences.
    """

    def __init__(self, input_path, fwd_trunc_pos, rev_trunc_pos, output_path, rep_seqs_path, stats_path,
                 fwd_trim_pos=0, rev_trim_pos=0, n_threads=0, msg=''):
        super().__init__(msg)
        self.input_path = input_path        # Path for the demultiplexed sequences to be denoised.
        self.fwd_trunc_pos = fwd_trunc_pos  # Position at which forward read sequences should be truncated.
        self.rev_trunc_pos = rev_trunc_pos  # Position at which reverse read sequences should be truncated.
        self.fwd_trim_pos = fwd_trim_pos    # Position at which forward read sequences should be trimmed.
        self.rev_trim_pos = rev_trim_pos    # Position at which reverse read sequences should be trimmed.
        self.n_threads = n_threads          # Number of threads to use. If 0 is provided, all cores are used.
        self.output_path = output_path      # Path for the resulting feature table.
        self.rep_seqs_path = rep_seqs_path  # Path for the resulting feature sequences.
        self.stats_path = stats_path        # Path for denoising statistics artifact.

    def __str__(self):
        return f"qiime dada2 denoise-paired \
               --i-demultiplexed-seqs {self.input_path} \
               --p-trunc-len-f {self.fwd_trunc_pos} \
               --p-trunc-len-r {self.rev_trunc_pos} \
               --p-trim-left-f {self.fwd_trim_pos} \
               --p-trim-left-r {self.rev_trim_pos} \
               --p-n-threads {self.n_threads} \
               --o-table {self.output_path} \
               --o-representative-sequences {self.rep_seqs_path} \
               --o-denoising-stats {self.stats_path}"
