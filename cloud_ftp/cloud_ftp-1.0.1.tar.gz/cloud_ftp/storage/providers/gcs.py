# Copyright 2017 Real Kinetic, LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

"""
Reaches out to GCS to download a file.  Bucket may or may not be specified.  If
not specified, default bucket is used.
"""
import cloudstorage
from cloudstorage.errors import NotFoundError

from google.appengine.api import app_identity

from cloud_ftp import error
from cloud_ftp.storage import StorageProvider


class GCSStorageProvider(StorageProvider):
    """Provides GCS storage from app engine.
    """
    def __init__(self, bucket=None):
        """Initializes GCS storage with the provided bucket in this project.
        If no bucket is provided, the default bucket is used.

        :param bucket: GCS bucket to use
        :type bucket: str or None
        """
        self._bucket = bucket or app_identity.get_default_gcs_bucket_name()

    def create_path(self, name):
        """Takes the provided name returns a fully qualified path to the file
        within a bucket.

        :param name: name of the file
        :type name: str
        :return: the fully qualified name
        :rtype: str
        """
        return '/{}/{}'.format(self._bucket, name)

    def fetch(self, name):
        """Calls GCS to look for the provided file name.  Returns a file handle
        that can be used to read the requested file.  The returned file *MUST*
        be closed.

        :param name: name of the file, not qualified
        :type name: str
        :return: file
        :rtype: File
        """
        path = self.create_path(name)
        try:
            return cloudstorage.open(path)
        except NotFoundError:
            raise error.FileNotFoundError(
                'unable to find gcs file: {}'.format(path)
            )
