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

import abc
import six


class FTPProvider(six.with_metaclass(abc.ABCMeta, object)):
    """Provides an interface to be used to talk to some external function or
    service to move data to GCS, thereby making it accessible to Google
    App Engine.

    Useful for many implementations, and for testing.
    """
    @abc.abstractmethod
    def move_file(self, ctx):
        """Should move the file from an FTP server to another service accessible
        from app engine.

        :return: The name of the moved file.
        :rtype: str
        """
        pass


class Context(object):
    def __init__(self, file_name, host, username=None, password=None):
        """Initializes the context with the provided information about the
        request.  Filename and host are required for the request, which
        are obvious, and username and password are optional.

        :param file_name: name of the file to transfer
        :type file_name: str
        :param host: FTP hostname
        :type host: str
        :param username: optional username when logging in
        :type username: str or None
        :param password: optional password if required
        :type password: str or None
        """
        self._file_name = file_name
        self._host = host
        self._username = username
        self._password=password

    @property
    def file_name(self):
        """Name of the file to transfer.

        :return: file name
        :rtype: str
        """
        return self._file_name

    @property
    def host(self):
        """Name of the FTP host.

        :return: FTP hostname
        :rtype: str
        """
        return self._host

    @property
    def username(self):
        """Optional username if the FTP server requires auth.

        :return: optional username
        :rtype: str or None
        """
        return self._username

    @property
    def password(self):
        """Optional password if the FTP server requires auth.

        :return: optional password
        :rtype: str or None
        """
        return self._password
