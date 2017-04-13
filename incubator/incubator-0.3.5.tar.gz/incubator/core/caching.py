import logging

from .constants import APP_NAME

logger = logging.getLogger(APP_NAME)


class ImageCache:
    def __init__(self):
        pass

    def add(self, image_id, parent_id, layer):
        logger.info('======> CACHE - SAVE\n')
        logger.debug('id: {}\nparent: {}\n{}\n'.format(str(image_id), str(parent_id), str(layer)))

    def get_layer(self, parent, layer):
        logger.info('======> CACHE - IMAGE NOT FOUND\n')
        logger.debug('parent: {}\n{}\n'.format(str(parent), str(layer)))
        return None
