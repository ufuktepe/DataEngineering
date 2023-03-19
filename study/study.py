import csv

from config import config
from study.invalid_study_error import InvalidStudyError
from static.layout import Layout
from utils import *


# Define titles for the manifest file.
MANIFEST_TITLES = {Layout.SINGLE: ['sample-id', 'absolute-filepath'],
                   Layout.PAIRED: ['sample-id', 'forward-absolute-filepath', 'reverse-absolute-filepath']}


class Study:
    """
    Represents a microbiome study that includes one or more fastq files and a metadata.
    """

    def __init__(self, parent_dir):
        self.parent_dir = parent_dir  # Parent directory for the study.
        self.metadata_path = None     # File path for the metadata file.
        self.manifest_path = None     # File path for the manifest file.
        self.layout = None            # Sequencing layout, single-end or paired-end reads.
        self.manifest_titles = []     # List of titles for the manifest file.

    def setup(self):
        """
        Initialize the study by identifying the metadata and number of reads per sample. Generate the manifest file.
        Raise an InvalidStudyError on error.
        """
        # Verify the directory is a valid path.
        if not os.path.isdir(self.parent_dir):
            raise InvalidStudyError(msg=f'{self.parent_dir} is an invalid directory!', parent_dir=self.parent_dir)

        # Identify the file path for metadata.
        try:
            self.metadata_path = self.get_metadata()
        except FileNotFoundError:
            raise InvalidStudyError(msg='No metadata found!', parent_dir=self.parent_dir)

        # Identify the sequencing layout (SINGLE or PAIRED).
        try:
            self.layout = self.extract_layout()
        except ValueError:
            raise InvalidStudyError(msg='Unable to identify the sequencing layout type!', parent_dir=self.parent_dir)

        # Generate the manifest file.
        try:
            self.manifest_path = self.generate_manifest_file()
        except FileNotFoundError:
            raise InvalidStudyError(msg='Unable to generate manifest file!', parent_dir=self.parent_dir)

    def get_dir(self):
        """
        Return the parent directory for the study.
        """
        return self.parent_dir

    def get_manifest_path(self):
        """
        Return the path for the manifest file. If the study is not set up then None will be returned.
        """
        return self.manifest_path

    def get_layout(self):
        """
        Return the sequencing layout. If the study is not set up then None will be returned.
        """
        return self.layout

    def get_metadata(self):
        """
        Return the first csv file found in the given directory. Raise a FileNotFoundError if no csv file exists.
        """
        for root, sub_dirs, file_names in os.walk(self.parent_dir):
            for file_name in file_names:
                if file_name.endswith(config.meta_data_ext):
                    return os.path.join(root, file_name)

        raise FileNotFoundError

    def extract_layout(self):
        """
        Extract the sequencing layout from the metadata and return it. Raise a ValueError if layout cannot be
        identified.
        """
        with open(self.metadata_path) as csv_file:
            # Create a dictionary from the csv file.
            for metadata_dict in csv.DictReader(csv_file):
                layout = metadata_dict.get(config.layout_title, '').lower()
                if layout == Layout.SINGLE:
                    return Layout.SINGLE
                elif layout == Layout.PAIRED:
                    return Layout.PAIRED

                raise ValueError

    def map_samples_to_files(self):
        """
        Return a dictionary that maps each sample to a list of fastq file paths.
        If the study includes single-end reads then each sample maps to a list that contains a single file path.
        If the study includes paired-end reads then each sample maps to a list that contains two file paths.
        """
        # Maps each sample to a list of absolute file paths.
        samples_to_files = {}

        # Get fastq file paths in the parent directory
        file_paths = get_file_paths(self.parent_dir, ext='fastq')

        # Iterate over each file and populate the samples_to_files dictionary.
        for file_path in file_paths:
            file_name = os.path.basename(file_path)

            # Skip the file if the file name has no underscores.
            if '_' not in file_name:
                continue

            sample_name = file_name.split('_')[0]

            # Add the sample name to samples_to_files if it doesn't already exist.
            if sample_name not in samples_to_files:
                samples_to_files[sample_name] = []

            samples_to_files[sample_name].append(file_path)

        return samples_to_files

    def generate_manifest_file(self):
        """
        Generate a manifest file that maps samples to fastq file paths. Raise a FileNotFoundError if samples cannot
        be mapped to fastq files.
        """
        # Map samples to fastq file paths.
        samples_to_files = self.map_samples_to_files()
        if not samples_to_files:
            raise FileNotFoundError

        # Identify the number of reads per sample
        n_reads = 1 if self.layout == Layout.SINGLE else 2

        manifest_path = os.path.join(self.parent_dir, 'manifest.tsv')

        # Create the manifest file.
        with open(manifest_path, 'w') as tsv_file:
            tsv_writer = csv.writer(tsv_file, delimiter='\t')
            # Print the titles based on reads per sample.
            tsv_writer.writerow(MANIFEST_TITLES[self.layout])
            for sample_id, file_paths in samples_to_files.items():
                # Skip the sample if reads per sample and the number of file paths do not match.
                if len(file_paths) != n_reads:
                    continue
                tsv_writer.writerow([sample_id, *file_paths])

        return manifest_path
