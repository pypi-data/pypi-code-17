
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

# Standard library modules.
import os
import glob
import warnings

# Third party modules.
from qtpy.QtCore import QResource
from qtpy.QtGui import QIcon

import pkg_resources

# Local modules.

# Globals and constants variables.

def init_resources():
    filepath = pkg_resources.resource_filename(__name__, 'tango.rcc')
    if not QResource.registerResource(filepath):
        warnings.warn('Could not register rcc: {}'.format(filepath))
        return
    QIcon.setThemeName('tango')

init_resources()