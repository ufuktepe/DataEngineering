import logging
import os
import shutil
import subprocess
import sys
import time

import pandas as pd

from pythonjsonlogger import jsonlogger


def get_file_paths(directory, ext):
    """
    Return a sorted list of file paths with the given extension in the directory including subdirectories.
    """
    files = []
    for root, sub_dirs, file_names in os.walk(directory):
        for file_name in file_names:
            if file_name.endswith(ext):
                files.append(os.path.join(root, file_name))
    files.sort()

    return files


def run_conda_command(cmd, env):
    """
    Run the shell command in the given conda environment.
    """
    cmd = f'/home/qiime2/miniconda/bin/conda run --no-capture-output -n {env} ' + cmd
    process = subprocess.run(cmd, shell=True)

    return process.returncode


def run_command(cmd):
    """
    Run the shell command.
    """
    process = subprocess.run(cmd, shell=True)

    return process.returncode


def create_dir(directory):
    """
    Create a new directory. Overwrite if it already exists.
    """
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


def copy_file(src, dst):
    """
    Copy the file from src to dst. Raise OSError if unsuccessful.
    """
    try:
        shutil.copy(src, dst)
    except:
        raise OSError


def get_runtime(start_time):
    """
    Compute the runtime based on the given start time and return it as a string.
    """
    end_time = time.time()
    delta = end_time - start_time
    hours = delta // 3600
    delta -= hours * 3600
    mins = delta // 60
    secs = delta - mins * 60

    return '%dh:%dm:%ds' % (hours, mins, secs)


def setup_logger(logger_name, logging_level):
    """
    Create a logger and return it.
    """
    logger = logging.getLogger(logger_name)

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    file_handler = logging.FileHandler(logger_name + '.log')

    stdout_format = logging.Formatter("%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(message)s")

    json_format = jsonlogger.JsonFormatter("%(name)s %(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s",
                                           datefmt="%Y-%m-%dT%H:%M:%SZ")

    stdout_handler.setFormatter(stdout_format)
    file_handler.setFormatter(json_format)

    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)

    logger.setLevel(logging_level)

    return logger


def create_txt(file_path, contents=''):
    """
    Create a text file.
    """
    with open(file_path, 'w') as f:
        if contents:
            f.write(contents)


def create_results_csv(feature_table_path, taxonomy_results_path, output_dir):
    """
    Create a csv file that includes Qiime2 results.
    """
    # Load the tsv files into dictionaries
    feature_table = pd.read_csv(feature_table_path, index_col=0, skiprows=1, sep='\t').to_dict()
    features_to_taxa = pd.read_csv(taxonomy_results_path, index_col=0, sep='\t').to_dict()

    # Validate the taxonomy results file
    if 'Taxon' not in features_to_taxa:
        raise ValueError(f'Taxon column is missing in {taxonomy_results_path}.')

    if 'Confidence' not in features_to_taxa:
        raise ValueError(f'Confidence column is missing in {taxonomy_results_path}.')

    csv_contents = []

    # Populate csv contents list
    for study_id, features_to_counts in feature_table.items():
        for feature, count in features_to_counts.items():
            try:
                taxon = features_to_taxa['Taxon'][feature]
                confidence = features_to_taxa['Confidence'][feature]
            except KeyError:
                raise ValueError(f'Feature ID {feature} is missing in {taxonomy_results_path}.')

            csv_contents.append(f'{study_id},{taxon},{confidence},{count}\n')

    # Create the csv file
    with open(os.path.join(output_dir, 'results.csv'), "w") as results:
        results.write('Run_ID,Taxon,Confidence,Count\n')
        results.writelines(csv_contents)


