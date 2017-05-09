import os
import sys
from confutil import Config
from .util import which

CONFIG = Config('commodore')


def home_config_path():
    return os.path.expanduser('~/.commodore.cfg')


def write_home_config():
    path = home_config_path()
    CONFIG.write(path)


def editor(path):
    editor = CONFIG.get('EDITOR', os.getenv('EDITOR'))
    if editor:
        # Gets rid of extra command line args, and python 2.7 compatible
        split = editor.split()
        return [which(split[0])] + split[1:] + [path]
    for editor in ('nano', 'pico', 'vim', 'vi', 'emacs'):
        editor_path = which(editor)
        if editor_path:
            return [editor_path, path]
    sys.exit('No text editor found! Please set ~/.commodore.cfg EDITOR '
             'variable to the path of a usable text editor.')
