"""
hn
Usage:
  hn hello
  hn top
  hn -h | --help
  hn --version
Options:
  -h --help                         Show this screen.
  --version                         Show version.
Examples:
  hn hello
  hn top
Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/shaddu/hn-cli
"""

from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import hn.commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items(): 
        if hasattr(hn.commands, k) and v:
            module = getattr(hn.commands, k)
            hn.commands = getmembers(module, isclass)
            command = [command[1] for command in hn.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
