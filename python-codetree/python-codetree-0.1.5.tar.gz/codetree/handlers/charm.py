import hashlib
import json
import logging
import os
import requests
import shutil
import subprocess
import tempfile
from six.moves.urllib.parse import urlparse

from .basic import HandlerResult, SourceHandler
from .exceptions import InvalidOption, NoSuchCharm


SUPPORTED_CHANNELS = ('unpublished', 'edge', 'beta', 'candidate', 'stable')


# Disable logging of unnecessary messages from request library and urllib3
# which is typically used by requests too
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class CharmStoreHandler(SourceHandler):
    """Download from charm store"""

    schemes = tuple(["cs"])
    metadata_filename = '.codetree_charmstore'

    def __init__(self, source):
        super(CharmStoreHandler, self).__init__(source)
        self.base_url = 'https://api.jujucharms.com/charmstore/v5'
        self.charmstore_url = None

    def get(self, dest, options):
        result = HandlerResult(False, source=self.source, dest=dest,
                               options=options)
        use_charm = True
        base_url = options.get('base_url')
        if base_url:
            try:
                parsed = urlparse(base_url)
            except Exception as err:
                raise InvalidOption('invalid base URL {}'.format(err))
            if parsed.scheme != 'https':
                raise InvalidOption('only https is supported for charm store base_url')
            use_charm = False
            self.base_url = base_url
        channel = options.get("channel", "stable")
        if channel not in SUPPORTED_CHANNELS:
            channels = ', '.join(SUPPORTED_CHANNELS)
            msg = 'Channel "{}" is invalid. Must be one of: {}.'.format(channel, channels)
            raise InvalidOption(msg)

        if use_charm and _have_charm_tools():
            downloader = _CharmStoreCharmDownloader(self.source, channel)
        else:
            downloader = _CharmStoreHttpDownloader(self.source, self.base_url, channel)

        self.charmstore_url = downloader.resolve()
        if os.path.exists(dest):
            if options.get("overwrite"):
                # Remove the directory even if it was previously a bzr or git
                # branch
                shutil.rmtree(dest)
            else:
                if self._source_with_channel(self.charmstore_url, channel) == self._get_url(dest):
                    logging.info("{} is up to date from url {}, skipping.".format(dest, self.charmstore_url))
                    result.success = True
                    return result

                # The version isn't up to date or is undetermined, if it isn't
                # a git/bzr repo then remove and continue
                if '.bzr' in os.listdir(dest) or '.git' in os.listdir(dest):
                    logging.info('Skipping existing dest {} because it looks like a bzr or git branch'.format(dest))
                    return result
                shutil.rmtree(dest)
        if downloader.get(dest):
            logging.info("{} charm retrieved from {}".format(dest, self.charmstore_url))
            self._set_url(dest, channel)
            result.success = True
        return result

    def _get_url(self, dest):
        """ Find the URL used to download the charm from the metadata.
        :param dest: Directory of downloaded charm to check url for
        :return: url with the channel as a string or None
        """
        path = os.path.join(dest, self.metadata_filename)
        if not os.path.exists(path):
            return None
        with open(path, 'r') as metadata_file:
            return metadata_file.read()

    def _set_url(self, dest, channel='stable'):
        """ Set the metadata on dest indicating it was downloaded from self.charmstore_url
        :param dest: The directory for which the charm url metadata will be set
        :param url: The resolved charm url
        :param channel: The channel the charm was downloaded from
        """

        path = os.path.join(dest, self.metadata_filename)
        with open(path, 'w') as metadata_file:
            metadata_file.write(self._source_with_channel(self.charmstore_url, channel))

    @staticmethod
    def _source_with_channel(url, channel):
        return '{};channel={}'.format(url, channel)


class _CharmStoreHttpDownloader(object):
    def __init__(self, source, base_url, channel='stable'):
        self.raw_source = source
        self.source = source[3:]
        self.base_url = base_url
        self.channel = channel

    def resolve(self):
        """ Discover/confirm the full charmstore URL including revision.
        """
        meta_url = "{}/{}/meta/id?channel={}".format(self.base_url, self.source, self.channel)
        try:
            self.charmstore_url = requests.get(meta_url).json()["Id"]
        except KeyError:
            raise NoSuchCharm('Could not find {!r} charm in the {!r} channel'.format(self.source, self.channel))
        return self.charmstore_url

    def get(self, dest):
        tmp_dir = tempfile.mkdtemp()
        try:
            logging.info("Downloading {} from charm store to {}".format(self.raw_source, dest))
            zipped_path = self.cs_download(tmp_dir)
            # Note python zipfile doesn't properly handle symbolic links use unzip instead
            subprocess.check_output(['unzip', zipped_path, '-d', dest], stderr=subprocess.STDOUT, universal_newlines=True)
            return True
        except Exception:
            raise
        finally:
            shutil.rmtree(tmp_dir)

    def cs_download(self, download_dir):
        """ Download an archive zip from the charm store and verify the SHA
            API docs are at:
            https://github.com/juju/charmstore/blob/v5-unstable/docs/API.md
        :param download_dir: The directory to download to
        :return: The full path of the downloaded zip file
        """
        # Remove 'cs:' to get expanded URL, which we actually want to use
        # for the download
        expanded_url = self.charmstore_url[3:]

        # Download (and verify SSL)
        req = requests.get("{}/{}/archive".format(self.base_url, expanded_url))
        zip_path = os.path.join(download_dir, 'charm.zip')
        with open(zip_path, 'wb') as charm_file:
            for chunk in req.iter_content(8192):
                charm_file.write(chunk)

        # Verify SHA
        expected_sha = req.headers['Content-Sha384']
        with open(zip_path, 'rb') as charm_file:
            calculated_sha = hashlib.sha384(charm_file.read()).hexdigest()
        if expected_sha != calculated_sha:
            raise requests.HTTPError("SHA of downloaded charm {} didn't match " +
                                     "expected SHA {}".format(calculated_sha,
                                                              expected_sha))

        return zip_path


class _CharmStoreCharmDownloader(object):
    def __init__(self, source, channel):
        self.source = source
        self.channel = channel

    def resolve(self):
        """ Discover/confirm the full charmstore URL including revision
        """
        cmd = ('charm', 'show', '--format=json', '--channel', self.channel, self.source, 'id')
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        try:
            self.charmstore_url = json.loads(out)['id']['Id']
        except KeyError:
            raise NoSuchCharm('Could not find {} charm in the {} channel'.format(self.source, self.channel))
        return self.charmstore_url

    def get(self, dest):
        logging.info("Downloading {} from charm store to {}".format(self.source, dest))
        cmd = ('charm', 'pull', '--channel', self.channel, self.source, dest)
        subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        return True


def _have_charm_tools():
    """ _have_charm_tools checks that there is an appropriate version of charm installed
        which can be used to fetch the charm.
    """
    try:
        subprocess.check_output(('charm', 'show', '--list'), stderr=subprocess.STDOUT)
    except (subprocess.CalledProcessError, OSError):
        return False
    return True
