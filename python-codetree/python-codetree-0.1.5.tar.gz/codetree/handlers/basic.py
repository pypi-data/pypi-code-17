import logging
import os
from six.moves.urllib.request import urlopen
from six.moves.urllib.error import URLError

import codetree.fileutils as fileutils


class HandlerResult(object):
    """ Holds the results from an a Handler get run and evaluates to False if the run failed.
    """
    def __init__(self, success, source=None, dest=None, revision=None, options={}):
        self.success = success
        self.source = source
        self.dest = dest
        self.revision = revision
        self.options = options

    def __bool__(self):
        return bool(self.success)

    def __nonzero__(self):
        return self.__bool__()

    def __str__(self):
        if self.source is None or self.dest is None:
            return ""

        line = "{}  {}".format(self.dest, self.source)
        options = self.options.copy()

        if self.revision is not None:
            options["revno"] = self.revision

        if len(options) > 0:
            option_strings = ["{}={}".format(key, value) for key, value in options.items()]
            line += ";" + ",".join(option_strings)

        return line


class SourceHandler(object):
    schemes = tuple()

    def __init__(self, source):
        """ The parent class for the various codetree sources
        :param source: The Source URL
        """
        self.source_raw = source
        self.source = source  # Some child classes modify self.source

    def get(self, dest, options):
        """ Retrieves the repository and writes to dest. This is the primary method called for all SourceHandlers.
        :param dest: The destination to write the repository to.
        :param options: A dictionary of possible configuration. revno and overwrite are the two options supported
                        by all handlers, others can be handler specific.
        :return: HandlerResult
        """
        raise NotImplementedError


class HttpFileHandler(SourceHandler):
    """Download plain files via http(s)"""

    schemes = (
        "http",
        "https",
    )

    def get(self, dest, options):
        result = HandlerResult(True, source=self.source_raw, dest=dest, options=options)
        if os.path.exists(dest):
            if options.get("overwrite"):
                os.unlink(dest)
            else:
                logging.info("Skipping existing dest {}".format(dest))
                return result
        logging.info("Downloading {} to {}".format(self.source, dest))
        try:
            response = urlopen(self.source)
        except URLError as e:
            logging.error("Failed to download {}: {}".format(self.source, e.reason))
            result.success = False
            return result
        with open(dest, "w") as f:
            f.write(response.read())
        return result


class LocalHandler(SourceHandler):
    """Copy local files. The special source '@' indicates that the destination
    is a directory."""

    schemes = (
        '',
        'file',
    )

    def get(self, dest, options):
        result = HandlerResult(True, source=self.source_raw, dest=dest, options=options)
        if self.source == "@":
            logging.info("Creating directory {}".format(dest))
            fileutils.mkdir(dest, overwrite=options.get("overwrite", False))
            return result

        method = options.get("method", "rsync")
        if method == "copy":
            logging.info("Copying {} to {}".format(self.source, dest))
            fileutils.copy(self.source, dest)
        elif method == "rsync":
            logging.info("Rsyncing {} to {}".format(self.source, dest))
            fileutils.rsync(self.source, dest)
        elif method == "link":
            logging.info("Creating symbolic link {} to {}".format(dest, self.source))
            fileutils.link(self.source, dest, overwrite=options.get(
                "overwrite", True))
        elif method == "hardlink":
            logging.info("Creating hard link {} to {}".format(dest, self.source))
            fileutils.link(self.source, dest, symbolic=False)

        return result
