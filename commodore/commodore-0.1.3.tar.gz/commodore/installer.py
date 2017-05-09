import os
from inter import Interact
from .config import CONFIG, home_config_path, write_home_config
from .util import cd, run


def is_installed():
    if not os.path.exists(home_config_path()):
        return False
    bin_path = CONFIG.get('BIN_DIR')
    if not bin_path:
        return False
    return os.path.exists(bin_path)


def make_git_dir(dir):
    with cd(dir):
        run('git init .')
        added = False
        for fname in os.listdir(dir):
            if fname == '.git':
                continue
            path = os.path.join(dir, fname)
            run('git add {}'.format(path))
            added = True
        if added:
            run('git commit -am "initial commit"')


def add_path_to_bashrc(bashrc=None):
    if not CONFIG['BIN_DIR'] or not os.path.exists(CONFIG['BIN_DIR']):
        return False
    new_line = 'export PATH={}:$PATH'.format(CONFIG['BIN_DIR'])
    if bashrc is None:
        bashrc = os.path.expanduser('~/.bashrc')
        if not os.path.exists(bashrc):
            bashrc = os.path.expanduser('~/.bash_profile')
            if not os.path.exists(bashrc):
                return False
    with open(bashrc) as f:
        lines = [x.strip() for x in f.readlines()]
    if new_line in lines:
        return True
    with open(bashrc, 'a') as f:
        f.write('\n{}\n'.format(new_line))
    return True


def install(force=False):
    inter = Interact()
    # Already installed, not force installing.
    if is_installed() and not force:
        return True
    # Not installed and didn't specify force so ask first.
    elif not (is_installed() or force):
        if not inter.ask_bool('Commodore not detected. Install?',
                              default=True):
            return False

    com_dir = inter.ask_path('where do you want commodore to save data?',
                             default='~/.commodore', creatable=True,
                             is_file=False)
    com_dir = os.path.expanduser(com_dir)

    if not os.path.exists(com_dir):
        os.mkdir(com_dir)

    bin_dir = os.path.join(com_dir, 'bin')
    if not os.path.exists(bin_dir):
        os.mkdir(bin_dir)

    git_dir = os.path.join(bin_dir, '.git')
    if not os.path.exists(git_dir):
        make_git_dir(bin_dir)

    editor = inter.ask_str('what editor do you want to use? (vim, emacs...)',
                           strip=True, default='vim')
    CONFIG['EDITOR'] = editor
    CONFIG['BIN_DIR'] = bin_dir
    add_path_to_bashrc()
    write_home_config()
    print('To change your editor or binary directory, edit your '
          '~/.commodore.cfg')
    return True
