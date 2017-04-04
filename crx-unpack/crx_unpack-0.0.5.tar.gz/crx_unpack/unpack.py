#!/usr/bin/env python3
"""
Usage: unpack.py [options] -c CRX_FILE [EXT_DIR] [PASSWD]
       unpack.py [options] xo ZIP_PATH EXT_DIR [PASSWD]
       unpack.py [options] convert BASE_DIR [-s SKIP_FORMAT ...]

Options:
 -c CRX_FILE  The extension file to extract.
 -f           Force extraction. Deletes the destination folder if it already
              exists.
 -t           Turns off testing the zip file portion before attempting
              extraction.
 -g           Don't skip converting GIFs when converting images to PNG format.
              By default, GIFs will be skipped because they cannot always be
              encoded to PNG format.
 -s SKIP_FORMAT ...
              Do not attempt to convert the given list of image formats. If
              multiple formats are given, the -s flag must precede each,
              e.g. -s ICO -s WEBP. [Default: ICO WEBP PNG]
 # --log-object=LOGOBJ
 #              Use the LOGOBJ for all log messages. Only has an effect when
 #              used with the `convert` option.

 --log-file=LOG_FILE
 --log-level=LOG_LEVEL
 --log-fmt=LOG_FMT
              Set the parameters for logging. Only has an effect when used
              with the `convert` option.

Unpacks the CRX_FILE by taking off the headers and extracting the zip file in
the same directory as the CRX_FILE. Optionally, unpacks to different directory
if EXT_DIR is specified.

With the `xo` command, only the extraction operation will take place. This
means the CRX header won't be parsed or tested, images won't be converted, and
the files' modes won't be changed.

With the `convert` command, all images in the BASE_DIR will be converted to
PNG format, except those specified with `-s`.
"""

import codecs
import logging
import os
import re
import sys
from os import path
from shutil import rmtree
from struct import Struct
from subprocess import check_call, CalledProcessError
from tempfile import NamedTemporaryFile
from zipfile import ZipFile, BadZipFile

from PIL import Image
from docopt import docopt

try:
    from crx_unpack.clr import add_color_log_levels
except ImportError:
    sys.path.append(path.abspath(path.join(path.dirname(__file__), '..')))
    from crx_unpack.clr import add_color_log_levels

__all__ = ['unpack', 'BadCrxHeader', 'BadZipFile']

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


class BadCrxHeader(Exception):
    """Raised when a CRX's header length or values aren't valid."""


def unpack(crx_file, ext_dir=None, overwrite_if_exists=False, img_tallies=None, test_contents=True, passwd=None,
           skip_img_formats=None, unpack_in_subprocess=False, convert_in_subprocess=True, do_convert=CONVERT_IMAGES):
    """
    Unpack the specified CRX (path) to the extraction directory at ext_dir.
    Return the absolute, normalized path to the extraction directory, useful
    if it wasn't given as a parameter.

    :param crx_file: Path to the CRX file.
    :type crx_file: str
    :param ext_dir: Directory where to extract the contents.
    :type ext_dir: str|None
    :param overwrite_if_exists: When extracting to a directory that already
        exists, unpack will normally fail. Setting this to True will delete
        the contents of the destination directory before unzipping.
    :type overwrite_if_exists: bool
    :param img_tallies: A dictionary for storing the number of each type of
        image file converted during the unpacking process.
    :type img_tallies: dict
    :param test_contents: When unpacking the CRX, use the zipfile module's
        test feature to test the validity of the embedded zip file before
        extraction.
    :type test_contents: bool
    :param passwd: Optional password to use when extracting the CRX.
    :type passwd: str
    :param skip_img_formats: The image formats to skip when attempting to
        convert them to PNG. This will typically include the strings ICO, PNG,
        and WEBP.
    :type skip_img_formats: list|tuple
    :param unpack_in_subprocess: Flag indicating if the job of unpacking the
        CRX should be done in a subprocess rather than calling the function
        directly. Usually this shouldn't need to be set as it will only hinder
        performance.
    :type unpack_in_subprocess: bool
    :param convert_in_subprocess: Flag indicating if the job of converting the
        images in the CRX should be done in a subprocess rather than calling
        the function directly. Usually this SHOULD be set, since converting
        images can sometimes cause a segmentation fault, which kills the whole
        process.
    :type convert_in_subprocess: bool
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
            logging.info('Created a named temp file at: {}'.format(zip_path))
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


def extract_zip(zip_file, extract_dir, pwd=None, test_contents=True):
    """
    Simple wrapper around the Python zipfile.ZipFile class.

    :param zip_file: Path to the zip file to be extracted.
    :type zip_file: str
    :param extract_dir: Directory where the contents will be extracted.
    :type extract_dir: str
    :param pwd: Password for the zip file.
    :type pwd: str|None
    :param test_contents: Whether to use the library's testzip() function on
        the archive before extracting. Tests if the CRC and header of each
        file in the archive are valid.
    :type test_contents: bool
    :return: None
    :rtype: None
    """
    # If we can read the state of the "extract only" command, use that to determine what we should do when we get an
    # error. True means the command was given, so we're only extracting, so we want to return a non-zero value when an
    # error occurs. If the script was imported, args won't be set and we'll get a NameError. In that case, we want to
    # just raise any of the errors that come up.
    try:
        just_exit = args['xo']
    except NameError:
        just_exit = False

    try:
        zip_obj = ZipFile(zip_file)
        if test_contents and zip_obj.testzip() is not None:
            # A file's CRC and/or header was invalid
            raise BadZipFile
        zip_obj.extractall(extract_dir, pwd=pwd)
    except ERR_TYPE[1:] as err:
        if not just_exit:
            raise
        for i in range(1, len(ERR_TYPE)):
            if isinstance(err, ERR_TYPE[i]):
                exit(i)


def set_mode(base_dir, file_mode=FILE_MODE, dir_mode=DIR_MODE):
    """Set file and dir permissions for everything under base_dir.

    :param base_dir: Top directory where to start working on changing the file
        and dir modes.
    :type base_dir: str
    :param file_mode: The permissions number to give all files in octal. The
        default is what Chrome OS uses on files.
    :type file_mode: int
    :param dir_mode: The permissions number to give all dirs in octal. The
        default is what Chrome OS uses on dirs.
    :type dir_mode: int
    :return: None
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

    :param num: Permissions number in octal, e.g. 644.
    :type num: int
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

    :param base_dir: The directory to walk through.
    :type base_dir: str
    :param skip_gifs: When True, GIFs won't be converted to preserve their
        animations.
    :type skip_gifs: bool
    :param skip_other: The image formats to skip when attempting to convert
        them to PNG. This will typically include the strings ICO, PNG, and
        WEBP.
    :type skip_other: list|tuple
    :param img_tallies: A dictionary for storing the number of each type of
        image file converted during the unpacking process.
    :type img_tallies: dict
    :return: None
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


if __name__ == '__main__':
    args = docopt(__doc__)

    # Make sure all of the specified formats is an accepted format
    Image.init()  # Make sure the list of supported types has been initialized
    _fs = []
    for _f in args['-s']:
        _f = _f.upper()
        if _f in Image.OPEN:
            _fs.append(_f)
    args['s'] = _fs.copy()
    # Always skip PNG files
    if 'PNG' not in args['-s']:
        args['-s'].append('PNG')

    if args['xo']:
        # Only do the extraction
        extract_zip(args['ZIP_PATH'], args['EXT_DIR'], pwd=args['PASSWD'], test_contents=(not args['-t']))

    elif args['convert']:
        # Only do the image conversion for a specific directory

        # Set up logging
        kw = {}
        if args['--log-file'] is not None:
            kw['filename'] = args['--log-file']
        if args['--log-level'] is not None:
            kw['level'] = int(args['--log-level'])
        if args['--log-fmt'] is not None:
            kw['format'] = args['--log-fmt']
        logging.basicConfig(**kw)
        add_color_log_levels(center=True)

        # Start the conversion
        convert_imgs(args['BASE_DIR'], skip_gifs=(not args['-g']), skip_other=args['-s'])

    else:
        _ext_dir = unpack(args['-c'], args['EXT_DIR'], args['-f'], test_contents=(not args['-t']),
                          passwd=args['PASSWD'], skip_img_formats=args['-s'])
        print("CRX extracted to: %s" % _ext_dir)
