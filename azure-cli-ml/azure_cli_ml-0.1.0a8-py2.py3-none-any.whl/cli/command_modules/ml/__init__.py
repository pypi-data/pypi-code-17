# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os.path
from pkg_resources import get_distribution, DistributionNotFound
import azure.cli.command_modules.ml._help #pylint: disable=unused-import



def load_params(_):
    import azure.cli.command_modules.ml._params #pylint: disable=redefined-outer-name
    try:
        from azure.cli.command_modules.machinelearning.cmd_execute import execute_arguments
        from azure.cli.command_modules.machinelearning.cmd_history import history_arguments
        from azure.cli.command_modules.machinelearning.cmd_computecontext import computecontext_arguments
        from azure.cli.command_modules.machinelearning.cmd_ambience import ambience_arguments
        from azure.cli.command_modules.machinelearning.cmd_project import project_arguments
        execute_arguments()
        history_arguments()
        computecontext_arguments()
        ambience_arguments()
        project_arguments()
    except ImportError:
        pass


def load_commands():
    import azure.cli.command_modules.ml.commands #pylint: disable=redefined-outer-name
    try:
        from azure.cli.command_modules.machinelearning.cmd_execute import execute_commands
        from azure.cli.command_modules.machinelearning.cmd_history import history_commands
        from azure.cli.command_modules.machinelearning.cmd_computecontext import computecontext_commands
        from azure.cli.command_modules.machinelearning.cmd_ambience import ambience_commands
        from azure.cli.command_modules.machinelearning.cmd_project import project_commands
        execute_commands()
        history_commands()
        computecontext_commands()
        ambience_commands()
        project_commands()
    except ImportError:
        pass

try:
    _dist = get_distribution('azure-cli-ml')
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(dist_loc):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'
else:
    __version__ = _dist.version