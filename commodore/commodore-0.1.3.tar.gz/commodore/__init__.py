'''
commodore

Manage and maintain your user's scripts and tools
'''

__title__ = 'commodore'
__version__ = '0.1.3'
__all__ = ()
__author__ = 'Johan Nestaas <johannestaas@gmail.com>'
__license__ = 'GPLv3+'
__copyright__ = 'Copyright 2017 Johan Nestaas'

import sys
from .installer import is_installed, install
from .cli import _main


def main():
    if not is_installed():
        # returns True if it successfully installs, otherwise user said No.
        if not install():
            sys.exit(1)
    else:
        _main()


if __name__ == '__main__':
    main()
