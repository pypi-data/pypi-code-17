import os
from confutil import Config
from .util import which

CONFIG = Config('commodore')


def home_config_path():
    return os.path.expanduser('~/.commodore.cfg')


def write_home_config():
    path = home_config_path()
    CONFIG.write(path)


def editor():
    if CONFIG.get('EDITOR'):
        return which(CONFIG['EDITOR'])
    if os.getenv('EDITOR'):
        return which(os.getenv('EDITOR'))
    for editor in ('nano', 'pico', 'vim', 'vi', 'emacs'):
        editor_path = which(editor)
        if editor_path:
            return editor_path
    return None
