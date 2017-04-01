#!/usr/bin/env python
#
# fetch_utils.py
# Utility funcgtions for fetching data files required by the dustmaps library.
#
# Copyright (C) 2016  Gregory M. Green
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from __future__ import print_function, division

from . import std_paths

import requests

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

import contextlib
import shutil
import hashlib
import json
import os
import os.path


# The URL of the Dataverse to use
#dataverse = 'https://demo.dataverse.org'
dataverse = 'https://dataverse.harvard.edu'


class Error(Exception):
    pass


class DownloadError(Error):
    """
    An exception that occurs while trying to download a file.
    """


def get_md5sum(fname, chunk_size=1024):
    """
    Returns the MD5 checksum of a file.

    Args:
        fname (str): Filename
        chunk_size (Optional[int]): Size (in Bytes) of the chunks that should be
            read in at once. Increasing chunk size reduces the number of reads
            required, but increases the memory usage. Defaults to 1024.

    Returns:
        The MD5 checksum of the file, which is a string.
    """

    def iter_chunks(f):
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

    sig = hashlib.md5()

    with open(fname, 'rb') as f:
        for chunk in iter_chunks(f):
            sig.update(chunk)

        # data = f.read()
        # return hashlib.md5(data).hexdigest()

    return sig.hexdigest()


def h5_file_exists(fname, size_guess=None, rtol=0.1, atol=1., dsets={}):
    """
    Returns ``True`` if an HDF5 file exists, has the expected file size, and
    contains (at least) the given datasets, with the correct shapes.

    Args:
        fname (str): Filename to check.
        size_guess (Optional[int]): Expected size (in Bytes) of the file. If
            ``None`` (the default), then filesize is not checked.
        rtol (Optional[float]): Relative tolerance for filesize.
        atol (Optional[float]): Absolute tolerance (in Bytes) for filesize.
        dsets (Optional[dict]): Dictionary specifying expected datasets. Each
            key is the name of a dataset, while each value is the expected shape
            of the dataset. Defaults to ``{}``, meaning that no datasets are
            checked.

    Returns:
        ``True`` if the file matches by all given criteria.
    """
    # Check if the file exists
    if not os.path.isfile(fname):
        # print('File does not exist.')
        return False

    # Check file size, withe the given tolerances
    if size_guess is not None:
        size = os.path.getsize(fname)
        tol = atol + rtol * size_guess

        if abs(size - size_guess) > tol:
            # print('File size is wrong:')
            # print('  expected: {: >16d}'.format(size_guess))
            # print('     found: {: >16d}'.format(size))
            return False

    # Check the datasets in the file
    if len(dsets):
        import h5py
        try:
            with h5py.File(fname, 'r') as f:
                for key in dsets:
                    # Check that dataset is in file
                    if key not in f:
                        # print('Dataset "{}" not in file.'.format(key))
                        return False
                    # Check that the shape of the dataset is correct
                    if dsets[key] is not None:
                        if f[key].shape != dsets[key]:
                            # print('Dataset "{}" has wrong shape:'.format(key))
                            # print('  expected: {}'.format(dsets[key]))
                            # print('     found: {}'.format(f[key].shape))
                            return False
        except IOError:
            # print('Problem reading file.')
            return False

    return True



def download_and_verify(url, md5sum, fname=None,
                        chunk_size=1024, clobber=False):
    """
    Download a file and verify the MD5 sum.

    Args:
        url (str): The URL to download.
        md5sum (str): The expected MD5 sum.
        fname (Optional[str]): The filename to store the downloaded file in.
            If `None`, infer the filename from the URL. Defaults to `None`.
        chunk_size (Optional[int]): Process in chunks of this size (in Bytes).
            Defaults to 1024.
        clobber (Optional[bool]): If `True`, any existing, identical file will
            be overwritten. If `False`, the MD5 sum of any existing file with
            the destination filename will be checked. If the MD5 sum does not
            match, the existing file will be overwritten. Defaults to `False`.

    Returns:
        The filename the URL was downloaded to.

    Raises:
        DownloadError: The MD5 sum of the downloaded file does not match
            `md5sum`.
        requests.exceptions.HTTPError: There was a problem connecting to the
            URL.
    """

    # Determine the filename
    if fname is None:
        fname = url.split('/')[-1]

    # Check if the file already exists on disk
    if (not clobber) and os.path.isfile(fname):
        md5_existing = get_md5sum(fname, chunk_size=chunk_size)
        if md5_existing == md5sum:
            print('File exists. Not overwriting.')
            return fname

    # Make sure the directory it's going into exists
    dir_name = os.path.dirname(fname)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    sig = hashlib.md5()

    if url.startswith('http://'):
        # Stream the URL as a file, copying to local disk
        with contextlib.closing(requests.get(url, stream=True)) as r:
            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError as error:
                print('Error connecting to URL: "{}"'.format(url))
                print(r.text)
                raise error

            with open(fname, 'wb') as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    sig.update(chunk)
    else: # e.g., ftp://
        with contextlib.closing(urlopen(url)) as r:
            with open(fname, 'wb') as f:
                while True:
                    chunk = r.read(chunk_size)

                    if not chunk:
                        break

                    f.write(chunk)
                    sig.update(chunk)


    if sig.hexdigest() != md5sum:
        raise DownloadError('The MD5 sum of the downloaded file is incorrect.\n'
                            + '  download: {}\n'.format(sig.hexdigest())
                            + '  expected: {}\n'.format(md5sum))

    return fname


def download(url, fname=None):
    """
    Downloads a file.

    Args:
        url (str): The URL to download.
        fname (Optional[str]): The filename to store the downloaded file in. If
            `None`, take the filename from the URL. Defaults to `None`.

    Returns:
          The filename the URL was downloaded to.

    Raises:
        requests.exceptions.HTTPError: There was a problem connecting to the
            URL.
    """
    # Determine the filename
    if fname is None:
        fname = url.split('/')[-1]

    # Stream the URL as a file, copying to local disk
    with contextlib.closing(requests.get(url, stream=True)) as r:
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print('Error connecting to URL: "{}"'.format(url))
            print(r.text)
            raise error

        with open(fname, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return fname


def dataverse_search_doi(doi):
    """
    Fetches metadata pertaining to a Digital Object Identifier (DOI) in the
    Harvard Dataverse.

    Args:
        doi (str): The Digital Object Identifier (DOI) of the entry in the
            Dataverse.

    Raises:
        requests.exceptions.HTTPError: The given DOI does not exist, or there
            was a problem connecting to the Dataverse.
    """

    url = '{}/api/datasets/:persistentId?persistentId=doi:{}'.format(dataverse, doi)
    r = requests.get(url)

    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print('Error looking up DOI "{}" in the Harvard Dataverse.'.format(doi))
        print(r.text)
        raise error

    return json.loads(r.text)


def dataverse_download_id(file_id, md5sum, **kwargs):
    url = '{}/api/access/datafile/{}'.format(dataverse, file_id)
    download_and_verify(url, md5sum, **kwargs)


def dataverse_download_doi(doi,
                           local_fname=None,
                           file_requirements={},
                           clobber=False):
    """
    Downloads a file from the Dataverse, using a DOI and set of metadata
    parameters to locate the file.

    Args:
        doi (str): Digital Object Identifier (DOI) containing the file.
        local_fname (Optional[str]): Local filename to download the file to. If
            `None`, then use the filename provided by the Dataverse. Defaults to
            `None`.
        file_requirements (Optional[dict]): Select the file containing the
            given metadata entries. If multiple files meet these requirements,
            only the first in downloaded. Defaults to `{}`, corresponding to no
            requirements.

    Raises:
        DownloadError: Either no matching file was found under the given DOI, or
            the MD5 sum of the file was not as expected.
        requests.exceptions.HTTPError: The given DOI does not exist, or there
            was a problem connecting to the Dataverse.

    """
    metadata = dataverse_search_doi(doi)

    def requirements_match(metadata):
        for key in file_requirements.keys():
            if metadata['dataFile'].get(key, None) != file_requirements[key]:
                return False
        return True

    for file_metadata in metadata['data']['latestVersion']['files']:
        if requirements_match(file_metadata):
            file_id = file_metadata['dataFile']['id']
            md5sum = file_metadata['dataFile']['md5']

            # print(json.dumps(file_metadata, indent=2, sort_keys=True))

            if local_fname is None:
                local_fname = file_metadata['dataFile']['filename']

            # Check if the file already exists on disk
            if (not clobber) and os.path.isfile(local_fname):
                md5_existing = get_md5sum(local_fname)
                if md5_existing == md5sum:
                    print('File exists. Not overwriting.')
                    return

            dataverse_download_id(file_id, md5sum,
                                  fname=local_fname, clobber=False)

            return

    raise DownloadError(
        'No file found under the given DOI matches the requirements.\n'
        'The metadata found for this DOI was:\n'
        + json.dumps(file_metadata, indent=2, sort_keys=True))


def download_demo():
    doi = '10.5072/FK2/ZSEMG9'
    requirements = {'filename': 'ResizablePng.png'}
    dataverse_download_doi(doi, file_requirements=requirements)


if __name__ == '__main__':
    download_planck()
