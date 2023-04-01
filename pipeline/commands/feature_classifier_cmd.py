from .command import Command


class FeatureClassifierCmd(Command):
    """
    Represents a command to classify reads by taxon using a classifier.
    """

    def __init__(self, input_path, classifier_path, output_path, n_jobs=-1, msg=''):
        super().__init__(msg)
        self.input_path = input_path            # Path for the feature data to be classified.
        self.classifier_path = classifier_path  # Path for the taxonomic classifier for classifying the reads.
        self.output_path = output_path          # Path for the output artifact.
        self.n_jobs = n_jobs                    # Maximum number of concurrent processes. If -1 all CPUs are used.

    def __str__(self):
        return f"qiime feature-classifier classify-sklearn \
               --i-reads {self.input_path} \
               --i-classifier {self.classifier_path} \
               --o-classification {self.output_path} \
               --p-n-jobs {self.n_jobs}"