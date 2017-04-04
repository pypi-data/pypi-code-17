"""Setup the readings logger."""

import os
import logging


DIR_LOGS = 'logs/'
PACKAGE_NAME = 'pydelaunator'


# Basic logging
logger = logging.getLogger(PACKAGE_NAME)
logger.setLevel(logging.DEBUG)


# Write in term
handler = logging.StreamHandler()
handler.setLevel(logging.WARNING)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


if os.path.exists('logs/'):
    # Write in file
    handler = logging.FileHandler(DIR_LOGS + '{}.logs'.format(PACKAGE_NAME))
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
