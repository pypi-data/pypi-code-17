"""Image processing code.

NOTE: all base64 string is encoded from binary data.
"""

import base64
import hashlib
import PIL.Image

import io
from cStringIO import StringIO
import numpy as np
""" IO """


def read_img_bin(img_fn):
  """Get image binary from an image file.

  Args:
    img_fn: image file path.
  Returns:
    image binary data.
  """
  with open(img_fn, "rb") as f:
    img_bin_data = f.read()
    return img_bin_data


def read_img_arr(img_fn):
  """Read image file to get ndarray.
  """
  img_bin = read_img_bin(img_fn)
  img_arr = img_bin_to_img_arr(img_bin)
  return img_arr


def write_img_arr(img_arr, save_fn):
  """Write image array to file.

  Args:
    img_arr: numpy array of image.
    save_fn: file to save image.
  """
  pil_img = img_arr_to_pil_img(img_arr)
  pil_img.save(save_fn)


""" Type convertion """


def img_bin_to_base64(img_bin):
  """Convert image binary data to base64.

  Args:
    img_bin: binary image data/string.
  Returns:
    base64 of image data.
  """
  img_base64 = base64.b64encode(img_bin)
  return img_base64


def img_bin_to_img_arr(img_bin, use_grayscale=False):
  """Convert image binary data to numpy array.

  Args:
    img_bin: binary image data.
    use_grayscale: convert to grayscale.
  Retunrs:
    numpy array: (height, width, chs).
  """
  pil_img = PIL.Image.open(StringIO(img_bin))
  if use_grayscale:
    new_img = pil_img.convert("L")
  else:
    new_img = pil_img.convert("RGB")
  return np.asarray(new_img)


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


def base64_to_img_arr(img_base64, use_grayscale=False):
  """Convert base64 image to rgb numpy array.

  Args:
    img_base64: base64 image string.
    use_grayscale: convert to grayscale.
  Returns:
    numpy array: (height, width, chs)
  """
  img_bin_str = base64_to_img_bin(img_base64)
  return img_bin_to_img_arr(img_bin_str, use_grayscale)


def base64_to_data_uri(img_base64):
  """For display in html.
  """
  datauri = "data:image/jpg;base64," + img_base64
  return datauri


def img_arr_to_pil_img(img_arr):
  """Convert numpy array image to pil image.
  """
  pil_img = PIL.Image.fromarray(img_arr)
  return pil_img


def pil_img_to_img_arr(pil_img, use_grayscale=False):
  """Convert pil image to numpy array.
  """
  if use_grayscale:
    new_img = pil_img.convert("L")
  else:
    new_img = pil_img.convert("RGB")
  return np.asarray(new_img)


def pil_img_to_img_bin(pil_img):
  """Convert pil image to binary string.
  """
  output = io.BytesIO()
  pil_img.save(output, format="JPEG")
  img_bin = output.getvalue()
  return img_bin


def show_img_arr(img_arr, title):
  """Display image array.

  Args:
    img_arr: numpy array of image.
    title: title name of the display window.
  """
  pil_img = PIL.Image.fromarray(img_arr)
  pil_img.show(title=title)


""" data processing. """


def get_new_dim(imgw, imgh, max_dim=400):
  """Get new image dimension with maximum constraint.

  Args:
    imgw: image width.
    imgh: image height.
    max_dim: maximum image dimension after.
  Returns:
    new img width and height.
  """
  new_imgw = imgw
  new_imgh = imgh
  if imgw > imgh:
    new_imgw = max_dim
    new_imgh = imgh * max_dim / imgw
  if imgh > imgw:
    new_imgh = max_dim
    new_imgw = imgw * max_dim / imgh
  return new_imgw, new_imgh
