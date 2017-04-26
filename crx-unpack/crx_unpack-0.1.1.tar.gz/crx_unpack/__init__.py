# *-* coding: utf-8 *-*
"""
The purpose of this module is to mimic how Google Chrome unpacks CRX files
as closely as possible. Involved in this is the need to remove the CRX headers
(see the structure details of CRXs on the :doc:`Home <index>` page), separate
the underlying ZIP file, extract the contents of the ZIP file, among other
things.

For end users, the only function you should need to call is :py:func:`unpack`,
which will handle each of the steps mentioned above.
"""

import codecs
import logging
import os
import re
from os import path
from shutil import rmtree
from struct import Struct
from subprocess import check_call, CalledProcessError
from tempfile import NamedTemporaryFile
from zipfile import ZipFile, BadZipFile

from PIL import Image

__all__ = ['unpack', 'BadCrxHeader', 'BadZipFile']

with open(path.abspath(path.join(path.dirname(__file__), 'VERSION'))) as _v:
    __version__ = _v.read().strip()

HEADER_FMT = Struct('<4s3I')
CONVERT_IMAGES = False
ERR_TYPE = (None,
            BadZipFile,
            MemoryError,
            IndexError,
            IsADirectoryError,
            NotADirectoryError)
DIR_MODE = 700
FILE_MODE = 644
JUST_EXIT = False


class BadCrxHeader(Exception):
    """Raised when a CRX's header length or values aren't valid."""


def unpack(crx_file, ext_dir=None, overwrite_if_exists=False, img_tallies=None, test_contents=True, passwd=None,
           skip_img_formats=None, unpack_in_subprocess=False, convert_in_subprocess=True, do_convert=CONVERT_IMAGES):
    """Unpack the CRX and extract it in the directory at ext_dir.

    Return the absolute, normalized path to the extraction directory (useful
    if it wasn't given as a parameter).

    :param str crx_file: Path to the CRX file.
    :param str ext_dir: Directory where to extract the contents.
    :param bool overwrite_if_exists: When extracting to a directory that already
        exists, unpack will normally fail. Setting this to True will delete
        the contents of the destination directory before unzipping.
    :param dict img_tallies: A dictionary for storing the number of each type of
        image file converted during the unpacking process.
    :param bool test_contents: When unpacking the CRX, use the zipfile module's
        test feature to test the validity of the embedded zip file before
        extraction.
    :param str passwd: Optional password to use when extracting the CRX. If the
        CRX was obtained from Google's `Chrome Web Store
        <https://chrome.google.com/webstore>`_, you should *not* need this. If
        you provide a password here, it will be passed on to the
        :py:func:`extract_zip` function.
    :param skip_img_formats: The image formats to skip when attempting to
        convert them to PNG. This will typically include the strings ICO, PNG,
        and WEBP.
    :type skip_img_formats: list or tuple
    :param bool unpack_in_subprocess: Flag indicating if the job of unpacking
        the CRX should be done in a subprocess rather than calling the function
        directly. Usually this shouldn't need to be set as it will only hinder
        performance.
    :param bool convert_in_subprocess: Flag indicating if the job of converting
        the images in the CRX should be done in a subprocess rather than calling
        the function directly. Usually this SHOULD be set, since converting
        images can sometimes cause a segmentation fault, which kills the whole
        process.
    :param bool do_convert: Flag indicating whether images should be converted
        during the unpacking process (intended to mimic Chrome's unpacking
        process more closely).
    :return: Directory where the archive was extracted.
    :rtype: str
    """
    if img_tallies is None:
        # This means that the calling function won't have access to these numbers, but for consistency's sake we'll
        # store them anyway.
        img_tallies = {}

    if skip_img_formats is None:
        skip_img_formats = []

    # Make sure the file exists, get basic info about it
    crx_file = path.abspath(crx_file)
    crx_dir, base = path.split(crx_file)
    crx_size = path.getsize(crx_file)  # Raises an error for us if the file doesn't exist
    if not re.search('\.crx$', base):
        raise OSError('File has unsupported extension, expected ".crx"')

    zip_path, signature, pub_key = [None] * 3
    with open(crx_file, 'rb') as fin:
        header_vals = fin.read(4 * 4)  # 4 values, each 4 bytes (32 bits) long
        if len(header_vals) < 16:
            raise BadCrxHeader('Invalid header length')
        magic, version, pup_key_len, sig_len = HEADER_FMT.unpack(header_vals)
        if magic != b'Cr24':
            raise BadCrxHeader('Invalid magic number: %s' % codecs.encode(magic, 'hex').decode('utf-8'))
        if version != 2:
            raise BadCrxHeader('Invalid version number: %d' % version)

        # Read in the public key and signature
        pub_key = fin.read(pup_key_len)
        signature = fin.read(sig_len)

        # TODO: Add verification methods for the public key and the signature
        # verify_pub_key(pub_key)
        # verify_signature(signature)

        # Detach zip file
        with NamedTemporaryFile('wb', suffix='.zip', delete=False) as fout:
            zip_path = fout.name
            logging.debug('Created a named temp file at: {}'.format(zip_path))
            # Read the rest of the file and save it as a .zip
            fout.write(fin.read())

    if None in (zip_path, signature, pub_key):
        raise IOError('Could not separate zip file from the CRX.')

    # Extract the zip file
    path.getsize(zip_path)
    if ext_dir is None:
        ext_dir = path.join(crx_dir, base.rsplit('.', 1)[0])
    ext_dir = path.abspath(ext_dir)

    if path.isdir(ext_dir):
        if overwrite_if_exists:
            # Delete the entire directory and its contents. Ignore errors because the files will likely
            # be overwritten upon unzip anyway.
            rmtree(ext_dir, ignore_errors=True)
        else:
            err = FileExistsError()
            err.errno = ''
            err.strerror = 'Cannot unpack CRX to directory that already exists'
            err.filename = ext_dir
            raise err

    if unpack_in_subprocess:
        prog = ['python3', __file__]
        if not test_contents:
            prog.append('-t')
        prog += ['xo', zip_path, ext_dir]
        if passwd is not None:
            prog.append(passwd)
        try:
            check_call(prog)
        except CalledProcessError as err:
            if 0 < err.returncode < len(ERR_TYPE):
                e = ERR_TYPE[err.returncode]()
                logging.warning('Got error of type "%s" while unpacking file at: %s' %
                                (e.__class__.__name__, ext_dir))
                # Re-raise the original exception
                raise ERR_TYPE[err.returncode]
            logging.warning('Got error of unknown type. Return code was: %d' % err.returncode)
            raise
    else:
        extract_zip(zip_path, ext_dir, pwd=passwd, test_contents=test_contents)

    if do_convert:
        if convert_in_subprocess:
            # Get the logger info so the subprocess can recreate it
            log_obj = logging.getLogger()
            fmt = log_obj.handlers[0].formatter._fmt
            log_file = log_obj.handlers[0].baseFilename
            level = log_obj.level

            # Create the subprocess
            prog = ['python3', __file__, 'convert', ext_dir, '--log-file=%s' % log_file, '--log-level=%s' % level,
                    '--log-fmt=%s' % fmt]
            for f in skip_img_formats:
                prog += ['-s', f]
            try:
                check_call(prog)
            except CalledProcessError:
                logging.warning('Image conversion subprocess failed while unpacking  %s' % crx_file)
                with open('failed_conversions.txt', 'a') as fout:
                    fout.write(crx_file + '\n')
        else:
            convert_imgs(ext_dir, img_tallies=img_tallies, skip_other=skip_img_formats)

    set_mode(ext_dir)  # Set mode after converting in case PIL changes things
    return ext_dir


def extract_zip(zip_file, extract_dir, pwd=None, test_contents=True, reraise_errors=not JUST_EXIT):
    """Simple wrapper around the Python zipfile.ZipFile class.

    Typically, it is not necessary to call this function directly from
    anywhere other than the :py:func:`unpack` function.

    :param str zip_file: Path to the zip file to be extracted.
    :param str extract_dir: Directory where the contents will be extracted.
    :param str pwd: Password for the zip file.
    :param bool test_contents: Whether to use the library's testzip() function
        on the archive before extracting. Tests if the CRC and header of each
        file in the archive are valid.
    :param bool reraise_errors: Set to False when the ``unpack`` script is run
        with the `xo` (extract only) command, in which case the function will
        return a non-zero value when an error occurs. The default, False,
        indicates that any errors that come up should just be re-raised.
    :rtype: None
    """
    try:
        zip_obj = ZipFile(zip_file)
        if test_contents and zip_obj.testzip() is not None:
            # A file's CRC and/or header was invalid
            raise BadZipFile
        zip_obj.extractall(extract_dir, pwd=pwd)
    except ERR_TYPE[1:] as err:
        if reraise_errors:
            raise
        for i in range(1, len(ERR_TYPE)):
            if isinstance(err, ERR_TYPE[i]):
                exit(i)


def set_mode(base_dir, file_mode=FILE_MODE, dir_mode=DIR_MODE):
    """Set file and dir permissions for everything under base_dir.

    :param str base_dir: Top directory where to start working on changing the
        file and dir modes.
    :param int file_mode: The permissions number to give all files in octal. The
        default is what Chrome OS uses on files.
    :param int dir_mode: The permissions number to give all dirs in octal. The
        default is what Chrome OS uses on dirs.
    :rtype: None
    """
    # Verify we're running in POSIX system first. No need to do this if we're in Windows.
    if os.name != 'posix':
        return

    # These are the file and dir permissions to set. File: 644  Dir: 700
    file_mode = _mode_from_num(file_mode)
    dir_mode = _mode_from_num(dir_mode)
    for root, dirs, files in os.walk(base_dir):
        for name in files:
            os.chmod(path.join(root, name), file_mode)
        for name in dirs:
            os.chmod(path.join(root, name), dir_mode)


def _mode_from_num(num):
    """Return the ORed stat objects representing the octal number num.

    :param int num: Permissions number in octal, e.g. 644.
    :return: The equivalent of bitwise ORing the permission constants in the
        stat library.
    :rtype: int
    """
    assert num > 100  # The user should at least be able to read the file...

    usr = int(num / 100)
    grp = int(num / 10) - usr * 10
    oth = num % 10

    return usr << 6 | grp << 3 | oth


def convert_imgs(base_dir, skip_gifs=True, skip_other=None, img_tallies=None):
    """Convert all images under base_dir to PNG format.

    Just like Chrome, the file extension remains unchanged. Also, GIFs are
    skipped to preserve their animations if skip_gifs is True.

    :param str base_dir: The directory to walk through.
    :param bool skip_gifs: When True, GIFs won't be converted to preserve their
        animations.
    :param skip_other: The image formats to skip when attempting to convert
        them to PNG. This will typically include the strings ICO, PNG, and
        WEBP.
    :type skip_other: list|tuple
    :param dict img_tallies: A dictionary for storing the number of each type of
        image file converted during the unpacking process.
    :rtype: None
    """
    if skip_other is None:
        skip_other = []

    if img_tallies is None:
        # This means that the calling function won't have access to these numbers, but for consistency's sake we'll
        # store them anyway.
        img_tallies = {}

    for root, dirs, files in os.walk(base_dir):
        for name in files:
            fname = path.join(root, name)

            # Check that it the file has a non-zero size
            if not path.getsize(fname):
                continue

            try:
                img = Image.open(fname)
            except OSError:
                # Means the file isn't an image
                pass
            except:
                logging.warning('Got unhandled exception during image conversion of file: %s' % fname, exc_info=1)
            else:
                # Increase the tally for this image type
                f = img.format
                if f not in img_tallies.keys():
                    img_tallies[f] = 0
                img_tallies[f] += 1

                # Don't attempt to convert certain types of images
                if skip_gifs and f == 'GIF':
                    continue
                if f in skip_other:
                    continue
                try:
                    # The save will fail in certain cases if the image isn't converted to RGBA mode, which is a
                    # normal RGB mode but with transparency. The palette of 'WEB' is a guess, but seemed a better
                    # option than the other one available for that function.
                    img.convert(mode='RGBA', palette='WEB').save(fname, format='PNG')
                except OSError:
                    # Means the file isn't an image or has no length
                    pass
                except:
                    logging.warning('Got unhandled exception while SAVING a converted image: %s' % fname, exc_info=1)


def verify_pub_key(pub_key):
    raise NotImplementedError


def verify_signature(sig):
    raise NotImplementedError
