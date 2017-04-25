"""
Core functionality of builder.
"""

import logging

import dockerfile_parse

from .commands import get_layers_from_dockerfile_structure
from .constants import APP_NAME
from .output import CHAPTER, SUBTITLE, TITLE
from .utils import ResultImage

logger = logging.getLogger(APP_NAME)


class Builder:
    """
    Class for building docker images.
    """

    def __init__(self, context, dockerfile, client, config, cache):

        self._dfp = dockerfile_parse.DockerfileParser(fileobj=dockerfile,
                                                      cache_content=True,
                                                      env_replace=False)

        self._context = context
        self._config = config
        self.client = client
        self._last_image = None
        self._cache = cache
        self._logs = []

    def build(self):
        """
        Builds an image from given Dockerfile, context and configuration.
        Using given container client.
        :return: id of final image
        """
        self._last_image = None
        self._logs = []
        self._prebuild()

        commands = self._dfp.structure
        layers = get_layers_from_dockerfile_structure(structure=commands,
                                                      layers_split_mark=self._config.layers,
                                                      build_context=self._context)

        for layer in layers:
            logger.info(TITLE.format(" LAYER {} ".format(layer.number)))
            cached_image = self._cache.get_layer(self._last_image, layer)
            if cached_image:
                self._last_image = cached_image
            else:
                self._create_new_layer(layer)
                for cmd in layer.commands:
                    cmd.apply(self.client, self._config)

                if not layer.is_last:
                    self._middle_commit(layer)

        self._final_commit(layers[-1])

        self._postbuild()

        return ResultImage(image_id=self._last_image, logs=self._logs)

    def _create_base_container(self):
        """
        Creates a base container filled in Dockerfile.
        :returns id of base container
        """
        image = self._dfp.baseimage
        logger.debug(CHAPTER.format("base image: {}".format(image)))

        if self._config.pull or self.client.get_image(image) is None:
            self.client.pull_image(image)

        return self.client.run_container_infinitely(
            image=image,
            infinite_command=self._config.infinite_command,
            volumes=self._config.volumes,
            container_limits=self._config.container_limits)

    def _create_new_layer(self, layer):
        if not self._last_image:
            layer.conf.current_container = self._create_base_container()
        else:
            layer.conf.current_container = self.client.run_container_infinitely(
                image=self._last_image,
                infinite_command=self._config.infinite_command,
                volumes=self._config.volumes,
                container_limits=self._config.container_limits)

    def _final_commit(self, layer):
        self.client.stop_container(layer.conf.current_container)
        logger.debug(TITLE.format(" FINAL COMMIT "))
        layer.conf.add_labels(self._config.labels)
        image = self.client.commit_container(layer.conf.current_container,
                                             conf=layer.conf.commit_config,
                                             author=layer.conf.author,
                                             message=layer.commit_message,
                                             tags=self._config.tags_and_repos)
        self._cache.add(image_id=image,
                        parent_id=self._last_image,
                        layer=layer)
        self._logs += layer.conf.logs
        self._last_image = image
        self.client.remove_container(layer.conf.current_container)

    def _middle_commit(self, layer):
        self.client.stop_container(layer.conf.current_container)
        logger.debug(TITLE.format(" COMMIT "))
        image = self.client.commit_container(layer.conf.current_container,
                                             conf=layer.conf.commit_config,
                                             author=layer.conf.author,
                                             message=layer.commit_message)

        self._cache.add(image_id=image,
                        parent_id=self._last_image,
                        layer=layer)
        self._logs += layer.conf.logs
        self._last_image = image
        self.client.remove_container(layer.conf.current_container)

    def _prebuild(self):
        """
        For future use.
        """
        logger.debug(SUBTITLE.format('prebuild'))

    def _postbuild(self):
        """
        For future use.
        """
        logger.debug(SUBTITLE.format('postbuild'))
