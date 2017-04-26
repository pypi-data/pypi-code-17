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

def fetch_ftp_file(ctx, ftp_provider, storage_provider):
    """Retrieves an FTP file using a two step process:
    1) Uses the FTP provider to move the FTP file from an FTP server to a GAE
    compatible data store.
    2) Uses the storage provider to reach out to that data store to retrieve
    the file.

    :param ctx: information about the request
    :type ctx: src.ftp.Context
    :param ftp_provider: ftp interface
    :type ftp_provider: src.ftp.FTPProvider
    :param storage_provider: storage interface
    :type storage_provider: src.storage.StorageProvider
    :return: file interface, this interface *must* be closed when done
    :rtype: File
    """
    name = ftp_provider.move_file(ctx)
    return storage_provider.fetch(name)
