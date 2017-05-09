import os
import shlex
import tempfile
from subprocess import check_output, call as _call
from contextlib import contextmanager


@contextmanager
def cd(dest_dir):
    old_dir = os.getcwd()
    os.chdir(os.path.expanduser(dest_dir))
    try:
        # code block in context
        yield
    finally:
        # return back to old dir
        os.chdir(old_dir)


def call(cmd):
    args = shlex.split(cmd)
    return _call(args)


def run(cmd):
    args = shlex.split(cmd)
    return check_output(args).decode('utf8')


def which(binary):
    path = run('which {}'.format(binary))
    return path.strip() or None


def edit_temp_file(init=''):
    with tempfile.NamedTemporaryFile(prefix='.commodore.', suffix='.tmp') as f:
        if init:
            f.write(init)
            f.flush()
        edit_file(f.name)
        f.seek(0)
        text = f.read().decode('utf8')
    return text


def edit_file(path):
    from .config import editor
    _call(editor(path))


def git_add_commit(name, message=None):
    from .config import CONFIG
    message = message or 'committing file {}'.format(name)
    with cd(CONFIG['BIN_DIR']):
        call('git add {}'.format(name))
        call('git commit -am \'{}\''.format(message.replace("'", '\\\'')))


def git_rm(name, message=None):
    from .config import CONFIG
    message = message or 'deleted {}'.format(name)
    with cd(CONFIG['BIN_DIR']):
        call('git rm {}'.format(name))
        call('git commit -am \'{}\''.format(message.replace("'", '\\\'')))
