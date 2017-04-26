#!/usr/bin/env python3
# *-* coding: utf-8 *-*
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

import logging

from docopt import docopt
from PIL import Image

import crx_unpack
from crx_unpack.clr import add_color_log_levels


def main():
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
        crx_unpack.extract_zip(args['ZIP_PATH'], args['EXT_DIR'], pwd=args['PASSWD'], test_contents=(not args['-t']),
                               reraise_errors=not args['xo'])

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
        crx_unpack.convert_imgs(args['BASE_DIR'], skip_gifs=(not args['-g']), skip_other=args['-s'])

    else:
        _ext_dir = crx_unpack.unpack(args['-c'], args['EXT_DIR'], args['-f'], test_contents=(not args['-t']),
                                     passwd=args['PASSWD'], skip_img_formats=args['-s'])
        print("CRX extracted to: %s" % _ext_dir)


if __name__ == '__main__':
    main()
