import codecs
import os
import sys
try:
  from setuptools import setup
except:
  from distutils.core import setup
def read(fname):
  return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()
NAME = "C-Viewer"
PACKAGES = []
DESCRIPTION = "package description."
LONG_DESCRIPTION = read("README.rst")
KEYWORDS = "comic Viewer"
AUTHOR = "gaianote"
AUTHOR_EMAIL = "gaianote@163.com"
URL = "http://gaianote.github.io"
VERSION = "0.0.1"
LICENSE = "MIT"
CLASSFIERS = ['License :: OSI Approved :: MIT License','Programming Language :: Python','Intended Audience :: Developers','Operating System :: OS Independent']
setup(
  name = NAME,
  version = VERSION,
  description = DESCRIPTION,
  long_description =LONG_DESCRIPTION,
  classifiers =  CLASSFIERS,
  keywords = KEYWORDS,
  author = AUTHOR,
  author_email = AUTHOR_EMAIL,
  url = URL,
  license = LICENSE,
  packages = PACKAGES,
  include_package_data=True,
  zip_safe=True,
)