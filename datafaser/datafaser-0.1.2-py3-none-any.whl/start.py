"""
Builds first run plan to load files given as arguments.
"""
import os

from datafaser.data_tree import DataTree
from datafaser.run import Runner
from datafaser import formats


def initialize_runner():
    """
    :return: datafaser.run.Runner instance complete with datafaser schema
    """
    runner = create_runner_to_load([get_schema_filepath()], 'load datafaser schema')
    runner.run_next_phase()
    return runner


def create_runner_to_load(files, phase_name):
    """
    :param files: list of paths to files or directories to load as data
    :return: datafaser.run.Runner configured to load given files
    """

    return Runner(DataTree(create_datafaser_structure_to_load_files(files, phase_name)))


def create_datafaser_structure_to_load_files(files, phase_name):
    """
    :param files: list of paths to files or directories to load as data
    :return: data structure containing plan to load files given as arguments
    """

    result = create_plan_to_load_files(files, phase_name)
    result['datafaser']['run']['done'] = []
    result['datafaser']['formats'] = formats.default_settings
    return result


def create_plan_to_load_files(files, phase_name):
    return {
        'datafaser': {
            'run': {
                'plan': [get_load_phase_for_files(files, phase_name)],
            }
        }
    }


def get_load_phase_for_files(files, phase_name):
    """
    :param files: list of paths to files or directories to load as data
    :return: data structure containing run plan phase to load files given as arguments
    """

    return {phase_name: [{
        'load': {
            'from': [{
                'files': files
            }]
        }
    }]}


def get_schema_filepath():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(this_dir, 'data')
