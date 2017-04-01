import platform
import os
import sys


def get_platform() -> str:
    if os.name == 'posix':
        if 'darwin' == sys.platform:
            return 'mac64'
        if 'linux' == sys.platform:
            arch = platform.architecture()[0]
            return '{}{}'.format('linux', arch[0:2])
