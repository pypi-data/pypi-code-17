import atexit
from setuptools                 import setup
from setuptools.command.install import install

def _post_install():
    import goosempl
    goosempl.copy_style()

class new_install(install):
    def __init__(self, *args, **kwargs):
        super(new_install, self).__init__(*args, **kwargs)
        atexit.register(_post_install)

__version__ = '0.1.3'

setup(
    name              = 'goosempl',
    version           = __version__,
    author            = 'Tom de Geus',
    author_email      = 'tom@geus.me',
    url               = 'https://github.com/tdegeus/GooseMPL',
    keywords          = 'matplotlib style',
    description       = 'Style and extension functions for matplotlib',
    long_description  = '',
    license           = 'MIT',
    install_requires  = ['matplotlib>=2.0.0'],
    packages          = ['goosempl'],
    cmdclass          = {'install': new_install},
    package_data      = {'goosempl/stylelib':[
        'goosempl/stylelib/goose-latex.mplstyle',
        'goosempl/stylelib/goose-tick-in.mplstyle',
        'goosempl/stylelib/goose-tick-lower.mplstyle',
        'goosempl/stylelib/goose.mplstyle'
    ]},
)

