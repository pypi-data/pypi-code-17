from distutils.core import setup
setup(
  name = 'EPICS-CA',
  packages=[""],
  package_dir={"":"EPICS_CA"},
  extra_path = "EPICS_CA",
  version = '2.0.3.15',
  description = 'EPICS Channel Access Protocol',
  author = 'Friedrich Schotte',
  author_email = 'friedrich.schotte@gmail.com',
  license = "GPLv3",
  url = 'https://github.com/friedrich-schotte/ca_python',
  download_url = 'https://github.com/friedrich-schotte/ca_python/archive/2.0.3.tar.gz',
  keywords = ['distributed instrumentation'], 
  classifiers = [],
)
