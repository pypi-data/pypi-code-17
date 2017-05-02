import logging

from .constants import APP_NAME
from .output import SUBTITLE

logger = logging.getLogger(APP_NAME)


class ImageCache:
    def __init__(self):
        pass

    def add(self, image_id, parent_id, layer):
        logger.info(SUBTITLE.format('CACHE - SAVE'))
        logger.debug('id: {}\nparent: {}\n{}\n'.format(str(image_id), str(parent_id), str(layer)))

    def get_layer(self, parent, layer):
        logger.info(SUBTITLE.format('CACHE - IMAGE NOT FOUND'))
        logger.debug('parent: {}\n{}\n'.format(str(parent), str(layer)))
        return None
