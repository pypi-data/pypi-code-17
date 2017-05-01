import os
import tarfile

from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import requests

def create_tar(output_filename, source_dir):
  with tarfile.open(output_filename, "w:gz") as tar:
    tar.add(source_dir, arcname=os.path.sep)


def upload_to_s3(url, tar_name, callback):
  # NOTE: This WILL NOT work in python 3.3.0 and 3.3.1
  # See:
  #  - http://bugs.python.org/issue16658
  #  - https://github.com/sigmavirus24/requests-toolbelt#known-issues

  encoder = MultipartEncoder(fields={'key': ('', tar_name), 'file': open(tar_name, 'rb')})
  monitor = MultipartEncoderMonitor(encoder, callback)

  req = requests.put(url, data=monitor)
  req.raise_for_status()
