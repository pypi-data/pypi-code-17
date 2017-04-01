"""Image processing code.
"""

import base64
import hashlib
import PIL.Image

from cStringIO import StringIO
import numpy as np


def read_img_bin(img_fn):
  """Get image binary from an image file.

  Args:
    img_fn: image file path.
  Returns:
    image binary data.
  """
  with open(img_fn, "rb") as f:
    return f.read()


def img_bin_to_base64(img_bin):
  """Convert image binary data to base64.

  Args:
    img_bin: binary image data/string.
  Returns:
    base64 of image data.
  """
  img_base64 = base64.b64encode(img_bin)
  return img_base64


def img_bin_to_numpy_rgb(img_bin):
  """Convert image binary data to numpy rgb array.

  Args:
    img_bin: binary image data.
  Retunrs:
    numpy array: (height, width, chs).
  """
  pil_img = PIL.Image.open(StringIO(img_bin))
  rgb_img = pil_img.convert("RGB")
  return np.asarray(rgb_img)


def base64_to_img_bin(img_base64):
  """Decode base64 image to binary string.

  Args:
    img_base64: base64 image string.
  Returns:
    binary image data.
  """
  img_bin = base64.b64decode(img_base64)
  # or: img_bin = img_base64.decode("base64")
  return img_bin


def base64_to_sha1(img_base64):
  """Hash base64 image to sha1.

  Args:
    img_base64: base64 string of image.
  Returns:
    sha1 of the image.
  """
  img_sha1 = hashlib.sha1(img_base64).hexdigest()
  return img_sha1


def base64_to_numpy_rgb(img_base64):
  """Convert base64 image to rgb numpy array.

  Args:
    img_base64: base64 image string.
  Returns:
    numpy array: (height, width, chs)
  """
  img_bin_str = base64_to_img_bin(img_base64)
  return img_bin_to_numpy_rgb(img_bin_str)


def base64_to_datauri(img_base64):
  """For display in html.
  """
  datauri = "data:image/jpg;base64," + img_base64
  return datauri
