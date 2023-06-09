import os

from . import utils
from .pipeline.commands.feature_table_merge_cmd import FeatureTableMergeCmd
from .pipeline.commands.feature_table_merge_taxa_cmd import FeatureTableMergeTaxaCmd
from .pipeline.commands.feature_table_summarize_cmd import FeatureTableSummarizeCmd
from .pipeline.commands.taxa_bar_plot_cmd import TaxaBarPlotCmd


def run(studies, output_dir, env):
    """
    Extract file paths from the given studies and merge the results in the output directory.
    """
    # Path for the merged feature table qza file.
    qza_table_path = os.path.join(output_dir, 'merged_feature_tables.qza')

    # Path for the merged feature table qzv file.
    qzv_table_path = os.path.join(output_dir, 'merged_feature_tables.qzv')

    # Path for the merged taxonomy results qza file.
    qza_taxonomy_path = os.path.join(output_dir, 'merged_taxonomy_results.qza')

    # Path for the merged taxonomy bar plot.
    taxonomy_bar_plot_path = os.path.join(output_dir, 'taxonomy_bar_plot.qzv')

    feature_table_paths = ''
    taxonomy_results_paths = ''

    # Build paths for feature tables and taxonomy results.
    for study in studies:
        feature_table_paths += study.feature_table_path + ' '
        taxonomy_results_paths += study.taxonomy_results_path + ' '

    # Generate the merged results.
    merge_feature_tables(feature_table_paths, qza_table_path, env)
    convert_feature_table(qza_table_path, qzv_table_path, env)
    merge_taxonomy_results(taxonomy_results_paths, qza_taxonomy_path, env)
    generate_taxonomy_bar_chart(qza_table_path, qza_taxonomy_path, taxonomy_bar_plot_path, env)


def merge_feature_tables(feature_table_paths, qza_table_path, conda_path, env):
    """
    Merge qza feature tables into a single qza feature table.
    """
    command = FeatureTableMergeCmd(input_path=feature_table_paths, output_path=qza_table_path)
    execute_conda_cmd(command, conda_path, env)


def convert_feature_table(qza_table_path, qzv_table_path, conda_path, env):
    """
    Convert the given feature table from qza to qzv.
    """
    command = FeatureTableSummarizeCmd(input_path=qza_table_path, output_path=qzv_table_path)
    execute_conda_cmd(command, conda_path, env)

    # Grant permission
    try:
        key = qzv_table_path.split('qiime2storage')[1][1:]
    except IndexError:
        raise ValueError
    permission_cmd = f'aws s3api put-object-acl --bucket qiime2storage --key {key}  --acl public-read'
    execute_shell_cmd(permission_cmd)


def merge_taxonomy_results(taxonomy_results_paths, qza_taxonomy_path, conda_path, env):
    """
    Merge qza taxonomy results into a single qza.
    """
    command = FeatureTableMergeTaxaCmd(input_path=taxonomy_results_paths, output_path=qza_taxonomy_path)
    execute_conda_cmd(command, conda_path, env)


def generate_taxonomy_bar_chart(qza_table_path, qza_taxonomy_path, taxonomy_bar_plot_path, conda_path, env):
    """
    Create a taxonomy bar chart from the given feature table and taxonomy results qza files.
    """
    command = TaxaBarPlotCmd(qza_table_path=qza_table_path,
                             qza_taxonomy_path=qza_taxonomy_path,
                             output_path=taxonomy_bar_plot_path)
    execute_conda_cmd(command, conda_path, env)

    # Grant permission
    try:
        key = taxonomy_bar_plot_path.split('qiime2storage')[1][1:]
    except IndexError:
        raise ValueError
    permission_cmd = f'aws s3api put-object-acl --bucket qiime2storage --key {key}  --acl public-read'
    execute_shell_cmd(permission_cmd)


def execute_conda_cmd(cmd, conda_path, env):
    """
    Execute the given command in the given environment.
    """
    return_code = utils.run_conda_command(cmd=str(cmd), conda_path=conda_path, env=env)
    if return_code != 0:
        raise ValueError(f'Qiime2 exited with return code {return_code}.')


def execute_shell_cmd(cmd):
    """
    Execute the given command.
    """
    return_code = utils.run_command(cmd=cmd)
    if return_code != 0:
        raise ValueError(f'Shell exited with return code {return_code}.')