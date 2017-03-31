""" main function """
from __future__ import print_function
import os
import argparse
import sys

from prompt_toolkit.history import FileHistory

import azclishell.configuration
import azclishell._dump_help
from azclishell.gather_commands import GatherCommands
from azclishell.app import Shell
from azclishell.az_completer import AzCompleter
from azclishell.az_lexer import AzLexer
from azclishell.util import default_style

from azure.cli.core.application import APPLICATION
from azure.cli.core._session import ACCOUNT, CONFIG, SESSION
from azure.cli.core._environment import get_config_dir as cli_config_dir
# from azure.cli.core.commands.client_factory import ENV_ADDITIONAL_USER_AGENT

AZCOMPLETER = AzCompleter(GatherCommands())
SHELL_CONFIGURATION = azclishell.configuration.CONFIGURATION


def main(args):
    """ the main function """
    # os.environ([ENV_ADDITIONAL_USER_AGENT]) = os.environ([ENV_ADDITIONAL_USER_AGENT]) + ' Shell'
    parser = argparse.ArgumentParser(prog='az-shell')
    parser.add_argument(
        '--no-style', dest='style', action='store_true', help='the colors of the shell')
    args = parser.parse_args(args)

    style = default_style()
    if args.style:
        style = None

    azure_folder = cli_config_dir()
    if not os.path.exists(azure_folder):
        os.makedirs(azure_folder)

    ACCOUNT.load(os.path.join(azure_folder, 'azureProfile.json'))
    CONFIG.load(os.path.join(azure_folder, 'az.json'))
    SESSION.load(os.path.join(azure_folder, 'az.sess'), max_age=3600)

    config = SHELL_CONFIGURATION

    if config.BOOLEAN_STATES[config.config.get('DEFAULT', 'firsttime')]:
        print("When in doubt, ask for 'help'")
        config.firsttime()

    shell_app = Shell(
        completer=AZCOMPLETER,
        lexer=AzLexer,
        history=FileHistory(
            os.path.join(SHELL_CONFIGURATION.get_config_dir(), config.get_history())),
        app=APPLICATION,
        styles=style
    )
    shell_app.run()


if __name__ == '__main__':
    main(sys.argv[1:])
