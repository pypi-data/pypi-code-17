import logging
from collections import OrderedDict

from .constants import APP_NAME
from .output import CHAPTER

logger = logging.getLogger(APP_NAME)


class ContainerHistory(object):
    def __init__(self):
        self._hist = OrderedDict()

    def add_container_status(self, id, state, message=None):
        debug_text = "container {}\n- id: {}".format(state, id)
        if message:
            debug_text += "\n{}".format(message)
        logger.debug(CHAPTER.format(debug_text))
        self._hist[id] = state

    def remove_container(self, id):
        logger.debug(CHAPTER.format("container removed\n- id: {}".format(id)))
        del self._hist[id]
