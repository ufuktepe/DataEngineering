from pipeline.commands.command import Command


class SingleDenoiseCmd(Command):
    """
    Represents a command to denoise single-end sequences.
    """

    def __init__(self, input_path, trunc_pos, output_path, rep_seqs_path, stats_path,
                 trim_pos=0, n_threads=0, msg=''):
        super().__init__(msg)
        self.input_path = input_path        # Path for the demultiplexed sequences to be denoised.
        self.trunc_pos = trunc_pos          # Position at which sequences should be truncated.
        self.trim_pos = trim_pos            # Position at which sequences should be trimmed.
        self.n_threads = n_threads          # Number of threads to use. If 0 is provided, all cores are used.
        self.output_path = output_path      # Path for the resulting feature table.
        self.rep_seqs_path = rep_seqs_path  # Path for the resulting feature sequences.
        self.stats_path = stats_path        # Path for denoising statistics artifact.

    def __str__(self):
        return f"qiime dada2 denoise-single \
               --i-demultiplexed-seqs {self.input_path} \
               --p-trunc-len {self.trunc_pos} \
               --p-trim-left {self.trim_pos} \
               --p-n-threads {self.n_threads} \
               --o-table {self.output_path} \
               --o-representative-sequences {self.rep_seqs_path} \
               --o-denoising-stats {self.stats_path}"
