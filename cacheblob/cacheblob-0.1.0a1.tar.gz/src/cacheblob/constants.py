# -*- coding: utf-8 -*-

"""This module contains constants and default values"""

import datetime

DEFAULT_DURATION = datetime.timedelta(days=14)
MEMOIZE_MAX_LENGTH = 10000
MEMOIZE_MAX_ENTRIES = None
DEFAULT_DB_FILE = "index.db"
DEFAULT_DIRECTORY = "data/"
IMPLEMENTED_HANDLERS = ['handler', 'plaintext', 'gzip', 'sqlite', 'mongo']
