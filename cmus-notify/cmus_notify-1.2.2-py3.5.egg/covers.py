# Copyright © 2017 Antoine Gagné
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Contains the code to extract album covers."""

import os.path

from .constants import DEFAULT_COVER_ART_PATH, DEFAULT_COVER_ART_DIMENSIONS

def find_artwork(audio_file_path):
    """Find the artwork corresponding to the given file path.

    :param audio_file_path: The path to the audio file
    :type audio_file_path: str
    :returns: A boolean indicating if the artwork could be found
    :rtype: bool
    """
    artwork_exist = True
    try:
        _save_artwork(audio_file_path)
    except Exception:
        artwork_exist = False

    return artwork_exist


def _save_mp4_artwork(audio_file_path):
    """Save the artwork of the corresponding mp4 or m4a file.

    :param audio_file_path: The path to the audio file
    :type audio_file_path: str
    :raises ImportError: If :module:`mutagen` or :module:`Pillow` are not installed
    """
    from mutagen import File
    from io import BytesIO
    audio_file = File(audio_file_path)
    cover = audio_file.tags['covr'][0]
    artwork = BytesIO(cover)
    _save_thumbnail_image(artwork)


def _save_mp3_artwork(audio_file_path):
    """Save the artwork of the corresponding mp3 file.

    :param audio_file_path: The path to the audio file
    :type audio_file_path: str
    :raises ImportError: If :module:`mutagen` is not installed
    """
    from mutagen import File
    from io import StringIO
    audio_file = File(audio_file_path)
    cover = None
    for tag, value in audio_file.tags.items():
        if tag.startswith('APIC:'):
            cover = value.data
    artwork = StringIO(cover)
    _save_thumbnail_image(artwork)

def _save_ogg_artwork(audio_file_path):
    """Save the artwork of the corresponding mp3 file.

    :param audio_file_path: The path to the audio file
    :type audio_file_path: str
    :raises ImportError: If :module:`mutagen` is not installed
    """
    from mutagen import File
    from io import BytesIO
    from base64 import b64decode
    import pdb
    audio_file = File(audio_file_path)
    cover = audio_file.tags['metadata_block_picture'][0]
    pdb.set_trace()
    artwork = BytesIO(b64decode(cover))
    _save_thumbnail_image(artwork)

def _save_thumbnail_image(image):
    """Save the corresponding image to a temporary location.

    :param image: The image to save
    :raises ImportError: If :module:`Pillow` is not installed
    """
    from PIL import Image
    picture = Image.open(image)
    picture.thumbnail(DEFAULT_COVER_ART_DIMENSIONS)
    picture.save(DEFAULT_COVER_ART_PATH, 'PNG')


#: Functions to save artwork depending on extensions
ARTWORK_SAVE_FUNCTIONS_BY_EXTENSION = {
    '.mp4': _save_mp4_artwork,
    '.m4a': _save_mp4_artwork,
    '.mp3': _save_mp3_artwork,
    '.ogg': _save_ogg_artwork
}


def _save_artwork(audio_file_path):
    """Save the artwork if it could be found.

    :param audio_file_path: The path to the audio file
    :type audio_file_path: str
    """
    _, extension = os.path.splitext(audio_file_path)
    ARTWORK_SAVE_FUNCTIONS_BY_EXTENSION[extension](audio_file_path)
