from .exceptions import PaparazzoError
from .paparazzo import Paparazzo
import logging

__title__ = 'paparazzo'
__version__ = '0.1.1'
__author__ = 'Ethan Bray'

# Create NullHandler if < Python 2.7
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

# Set default handler to avoid 'No handler found' warnings
logging.getLogger(__name__).addHandler(NullHandler())
