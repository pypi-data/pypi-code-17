import os
import sys
import logging
import argparse

from eva.utils.importlib import import_module
from eva.conf import settings
from eva.utils.findapps import App

CURDIR = os.path.dirname(os.path.realpath(__file__))


# cache
MAP_COMMANDS = {}


def exec_command_file(filepath):
    global_namespace = {
        "__file__": filepath,
        "__name__": "__main__",
    }
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), global_namespace)
    return global_namespace.get('Command')


def _load_commands(name, cmdDir):

    global MAP_COMMANDS

    LOCAL_COMMANDS = {}

    if not os.path.isdir(cmdDir):
        logging.warn('{0} is not a directory'.format(cmdDir))
        return

    for f in os.listdir(cmdDir):
        if not f.endswith('.py'):
            continue

        if f.startswith('__'):
            continue

        cmdFile = os.path.join(cmdDir, f)
        Command = exec_command_file(cmdFile)

        if not Command:
            logging.warn('%s is not a Command Module!', cmdFile)
            continue

        c = Command()

        if not (hasattr(c, 'cmd') and
                hasattr(c, 'help') and
                hasattr(c, 'run')):
            logging.warn('%s is not a Command Module!',
                         os.path.join(CURDIR, f))
            continue

        LOCAL_COMMANDS[c.cmd] = c

    if LOCAL_COMMANDS:
        MAP_COMMANDS[name] = LOCAL_COMMANDS


def load_commands():
    global MAP_COMMANDS

    if len(MAP_COMMANDS) == 0:
        _load_commands('core', os.path.join(CURDIR, 'commands'))

        for app_name in settings.INSTALLED_APPS:
            app = App(app_name)

            dc = os.path.join(app.abspath, 'management/commands')
            if os.path.isdir(dc):
                _load_commands(app.fullname, dc)

        for cmdDir in settings.MANAGEMENT_COMMAND_DIRS:
            _load_commands('custom', cmdDir)


def print_usage():
    print('''{prog} - Eva Management Tools

Usage:

    {prog} NAMESPACE COMMAND OPTIONS

Help:

    {prog} help | -h | --help

Command:

'''.format(prog=sys.argv[0]))
    global MAP_COMMANDS
    for name in MAP_COMMANDS:
        print('[{0}]'.format(name))
        cmds = MAP_COMMANDS[name]
        for k in cmds:
            c = cmds[k]
            print('    {cmd:16} {help}'.format(cmd=c.cmd, help=c.help))
        print('')

    print('''
Example:

    # 同步/创建/初始化数据库
    {prog} core syncdb --db-echo

    # core 类型的 namespace 可以省略，因此上一条命令等于
    {prog} syncdb --db-echo
'''.format(prog=sys.argv[0]))


def main(argv=sys.argv[1:]):

    load_commands()

    if len(argv) < 1:
        print_usage()
        sys.exit(1)

    namespace = argv[0]

    # nice hack!
    if namespace.startswith('app.') or namespace == 'core':
        if len(argv) < 2:
            print_usage()
            sys.exit(1)
        else:
            cmd = argv[1]
            argv = argv[2:] if len(argv) > 1 else []
    else:
        namespace = 'core'
        cmd = argv[0]
        argv = argv[1:] if len(argv) > 0 else []

    global MAP_COMMANDS

    if namespace in MAP_COMMANDS:
        cmds = MAP_COMMANDS[namespace]
        if cmd in cmds:
            cmds[cmd](argv)
            return

    if cmd in ['help', '-h', '--help']:
        print_usage()

    else:
        print('unknown cmd: ', cmd)
