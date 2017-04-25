"""
The MIT License (MIT)

Copyright (c) 2017 Frantisek Lachman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Python API for the alternative docker builder.
"""
import logging

from .core import utils
from .core.build import Builder
from .core.caching import ImageCache
from .core.client import DockerClient
from .core.config import ImageConfig
from .core.constants import APP_NAME
from .core.context import BuildContext
from .core.output import ERROR_SUBTITLE

logger = logging.getLogger(APP_NAME)


def build(path=None, fileobj=None, tag=None,
          custom_context=False, pull=False, rm=False,
          forcerm=False, dockerfile=None, buildargs=None,
          container_limits=None, volumes=None,
          labels=None, config=None, context_file_limit=None,
          container_client=None, cache=None):
    """

    :param path: (str) Path to the directory containing the Dockerfile.
    :param fileobj: A file object to use as the Dockerfile. (Or a file-like
                object)
    :param tag: (str or list) A tag to add to the final image.
    :param custom_context: (bool) Optional if using ``fileobj``.
    :param pull: (bool) Downloads any updates to the FROM image in Dockerfiles.
    :param rm: (bool) Remove intermediate containers. The ``docker build``
                command now defaults to ``--rm=true``, but we have kept the old
                default of `False` to preserve backward compatibility.
    :param forcerm: (bool) Always remove intermediate containers,
                        even after unsuccessful builds
    :param dockerfile: (str) A path within the build context to the Dockerfile.
    :param buildargs:  (dict) A dictionary of build arguments.
    :param container_limits: (dict) A dictionary of limits applied to each
                container created by the build process. Valid keys:

                - memory (int): set memory limit for build
                - memswap (int): Total memory (memory + swap), -1 to disable
                    swap
                - cpushares (int): CPU shares (relative weight)
                - cpusetcpus (str): CPUs in which to allow execution, e.g.,
                    ``"0-3"``, ``"0,1"``
    :param labels: (dict) A dictionary of labels to set on the image.
    :param volumes: (dict) A dictionary of bind volumes.
    :param config: (dict or list of dicts) A dictionary of addition configuration.
    :param context_file_limit: (int) Maximum size of in memory config. (0 is unlimited and default)
    :param cache: object responsible for caching images
    :param container_client: client representing basic API
    :return: id of created image
    """

    try:
        container_client = container_client or DockerClient()
    except Exception as ex:
        logger.warning(ERROR_SUBTITLE.format("Cannot launch container client:\n{}".format(ex)))
        raise ex

    cache = cache or ImageCache()

    try:
        config_object = ImageConfig.merge_configs(config)
    except Exception as ex:
        logger.warning(ERROR_SUBTITLE.format("Cannot merge config files:\n{}".format(ex)))
        raise ex

    try:
        config_object.update(buildargs=buildargs,
                             container_limits=container_limits,
                             context_file_limit=context_file_limit,
                             forcerm=forcerm,
                             labels=labels,
                             pull=pull,
                             rm=rm,
                             tags=tag,
                             volumes=volumes)
    except Exception as ex:
        logger.warning(ERROR_SUBTITLE.format("Cannot update config with arguments:\n{}".format(ex)))
        raise ex

    try:
        context_fileobj, dockerfile_fileobj = utils.mkbuildcontext(path=path,
                                                                   fileobj=fileobj,
                                                                   custom_context=custom_context,
                                                                   dockerfile=dockerfile,
                                                                   client=container_client,
                                                                   limit=config_object.context_file_limit)
        build_context = BuildContext(context=context_fileobj, limit=context_file_limit)

    except Exception as ex:
        logger.warning(ERROR_SUBTITLE.format("Cannot make build context:\n{}".format(ex)))
        raise ex

    try:
        builder = Builder(context=build_context,
                          dockerfile=dockerfile_fileobj,
                          client=container_client,
                          config=config_object,
                          cache=cache)
        return builder.build()
    except Exception as ex:
        logger.warning(ERROR_SUBTITLE.format("Build failed:\n{}".format(ex)))
        raise ex
