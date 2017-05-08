import os
import sys
from .config import CONFIG
from .util import edit_temp_file, git_add_commit, edit_file, git_rm


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
    new_script = edit_temp_file()
    with open(path, 'w') as f:
        f.write(new_script)
    os.chmod(path, 0o775)
    git_add_commit(path, message='new script called {}'.format(name))
    print('New script added at {}'.format(path))


def _edit(name):
    path = os.path.join(CONFIG['BIN_DIR'], name)
    if not os.path.exists(path):
        sys.exit('script {} does not exist'.format(name))
    edit_file(path)
    git_add_commit(name, message='edited script {}'.format(name))
    print('Successfully edited {}'.format(name))


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

    p = subs.add_parser('create')
    p.add_argument('script_name')

    p = subs.add_parser('list')

    p = subs.add_parser('edit')
    p.add_argument('script_name')

    p = subs.add_parser('delete')
    p.add_argument('script_name')

    args = parser.parse_args()

    if args.cmd == 'list':
        _list()
    elif args.cmd == 'create':
        _create(args.script_name)
    elif args.cmd == 'edit':
        _edit(args.script_name)
    elif args.cmd == 'delete':
        _delete(args.script_name)
    else:
        parser.print_usage()
        sys.exit(1)
