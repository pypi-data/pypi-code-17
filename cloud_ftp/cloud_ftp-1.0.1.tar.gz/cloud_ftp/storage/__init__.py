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


class StorageProvider(six.with_metaclass(abc.ABCMeta, object)):
    """Provides the interface into reaching out an external storage service
    and downloading a file.  This can be any service accessible from Google
    App Engine.
    """
    @abc.abstractmethod
    def fetch(self, name):
        """Fetches the file associated with the provided name.  Raises a file
        not found error if the requested file could not be found.

        :param name: name of the file
        :type name: str
        :return: file handle
        :rtype: File
        """
        pass
