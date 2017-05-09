import os
import sys
from .config import CONFIG
from .util import git_add_commit, edit_file, git_rm, cd, call


def _git(args):
    args = 'git ' + args
    with cd(CONFIG['BIN_DIR']):
        call(args)


def _list():
    bin_dir = CONFIG['BIN_DIR']
    for fname in os.listdir(bin_dir):
        if fname == '.git':
            continue
        print(fname)


def _create(name):
    path = os.path.join(CONFIG['BIN_DIR'], name)
    if os.path.exists(path):
        sys.exit('script already exists - choose another name or run "edit"')
    edit_file(path)
    if os.path.exists(path):
        os.chmod(path, 0o775)
        git_add_commit(path, message='new script called {}'.format(name))
        print('New script added at {}'.format(path))
    else:
        print('File unwritten.')


def _edit(name):
    path = os.path.join(CONFIG['BIN_DIR'], name)
    if not os.path.exists(path):
        sys.exit('script {} does not exist'.format(name))
    edit_file(path)
    if os.path.exists(path):
        git_add_commit(name, message='edited script {}'.format(name))
        print('Successfully edited {}'.format(name))
    else:
        sys.exit('File disappeared while editing!')


def _delete(name):
    path = os.path.join(CONFIG['BIN_DIR'], name)
    if not os.path.exists(path):
        sys.exit('script {} does not exist'.format(name))
    git_rm(name)
    print('Successfully deleted {}'.format(name))


def _main():
    import argparse
    parser = argparse.ArgumentParser('commodore')
    subs = parser.add_subparsers(dest='cmd')

    p = subs.add_parser('create', help='create a new script')
    p.add_argument('script_name')

    p = subs.add_parser('list', help='list your scripts')

    p = subs.add_parser('edit', help='edit a script')
    p.add_argument('script_name')

    p = subs.add_parser('delete', help='delete a script')
    p.add_argument('script_name')

    p = subs.add_parser('git', help='run a git command in the bin repo')
    p.add_argument('git_args')

    args = parser.parse_args()

    if args.cmd == 'list':
        _list()
    elif args.cmd == 'create':
        _create(args.script_name)
    elif args.cmd == 'edit':
        _edit(args.script_name)
    elif args.cmd == 'delete':
        _delete(args.script_name)
    elif args.cmd == 'git':
        _git(args.git_args)
    else:
        parser.print_usage()
        sys.exit(1)
