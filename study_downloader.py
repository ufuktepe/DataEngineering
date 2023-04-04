import os
import sys
import time

import utils
from config import config


def download_data():
    # Check arguments.
    if len(sys.argv) != 5:
        print('Please provide an input text file, a metadata,an output directory, and a scratch directory.')
        return

    input_txt_path = sys.argv[1]
    metadata_path = sys.argv[2]
    output_dir = sys.argv[3]
    scratch_dir = sys.argv[4]

    try:
        validate(input_txt_path, metadata_path, output_dir, scratch_dir)
    except ValueError:
        return

    # Set up the configuration
    try:
        config.setup()
    except FileExistsError:
        print('Configuration file is missing.')
        return

    # Get the metadata file name
    metadata_f_name = os.path.basename(metadata_path)

    with open(input_txt_path, 'r') as f:
        study_ids = [s.strip() for s in f.readlines()]

    for study_id in study_ids:
        start_time = time.time()

        study_dir = os.path.join(output_dir, study_id)

        # Skip if folder already exists
        if os.path.exists(study_dir):
            print(f'{study_dir} already exists.')
            continue

        os.mkdir(study_dir)

        # Download the study files
        print(f'Downloading {study_dir}...')
        return_code = utils.run_conda_command(cmd=f'fasterq-dump {study_id} -O {study_dir} -t {scratch_dir}', env=config.env)
        print(return_code)

        if return_code != 0:
            print(f'Error in downloading {study_id}.')
            continue

        # Copy the metadata
        try:
            utils.copy_file(src=metadata_path, dst=os.path.join(study_dir, metadata_f_name))
        except OSError:
            print(f'Unable to copy the metadata for {study_dir}.')
            continue

        # Create the complete.txt file
        with open(os.path.join(study_dir, 'complete.txt'), 'w') as _:
            pass

        print(f'Downloaded {study_id} in {utils.get_runtime(start_time)}.')


def validate(input_txt_path, metadata_path, output_dir, scratch_dir):
    if not input_txt_path.endswith('.txt'):
        print('Please provide a valid input text file.')
        raise ValueError

    if not metadata_path.endswith('.csv'):
        print('Please provide a valid metadata file.')
        raise ValueError

    if not os.path.isdir(output_dir):
        print('Please provide a valid output directory.')
        raise ValueError

    if not os.path.isdir(scratch_dir):
        print('Please provide a valid scratch directory.')
        raise ValueError


if __name__ == '__main__':
    download_data()