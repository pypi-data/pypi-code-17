try:
    # python 2.x
    from dict_config_parser import DictConfigParser
except ImportError:
    # python 3.x
    from configparser import ConfigParser

from .config_generator import generate_config
from .config_generator import get_config_vars
from .fs_commands import mkdirp
from .simple_version import get_major_version
from .simple_version import get_minor_version
from .simple_version import get_minor_version_with_increment
from .package_generator import package
from .vcs_info import get_commit_rev
from .vcs_info import get_branch
