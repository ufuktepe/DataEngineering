import os
import sys
import shutil
import subprocess
import time

import logging
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

def run_command(cmd, env):
    """
    Run the shell command in the given conda environment.
    """
    cmd = f'conda run --no-capture-output -n {env} ' + cmd
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

def setup_logger(logger_name, logger_path):
    """
    Create a logger and return it.
    """
    logger = logging.getLogger(logger_name)

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    file_handler = logging.FileHandler(logger_path)

    stdout_format = logging.Formatter("%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(message)s")

    json_format = jsonlogger.JsonFormatter("%(name)s %(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s",
                                           datefmt="%Y-%m-%dT%H:%M:%SZ")

    stdout_handler.setFormatter(stdout_format)
    file_handler.setFormatter(json_format)

    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)

    logger.setLevel(logging.DEBUG)

    return logger

def is_study_ready(file_names):
    """
    Check if the given list of file names include a csv file, a fastq file, a complete.txt file and doesn't include a
    processed.txt file. If so then return true. Otherwise, return false.
    """
    has_csv = False
    is_download_complete = False
    has_fastq = False

    for file_name in file_names:
        if file_name.endswith('.csv'):
            has_csv = True
        elif file_name.endswith('.fastq'):
            has_fastq = True
        elif file_name == 'complete.txt':
            is_download_complete = True
        elif file_name == 'processed.txt':
            return False

        if has_csv and is_download_complete and has_fastq:
            return True

    return False