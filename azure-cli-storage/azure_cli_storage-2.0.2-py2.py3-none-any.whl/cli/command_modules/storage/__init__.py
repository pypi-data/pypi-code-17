# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import azure.cli.command_modules.storage._help  # pylint: disable=unused-import


def load_params(_):
    import azure.cli.command_modules.storage._params  # pylint: disable=redefined-outer-name


def load_commands():
    import azure.cli.command_modules.storage.commands  # pylint: disable=redefined-outer-name
