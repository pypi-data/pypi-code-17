from distutils.core import setup
setup(
  name = 'digitrecklib',
  packages = ['digitrecklib'], # this must be the same as the name above
  version = '0.2.1',
  package_data={'digitrecklib': ['core/*.py', "*.py"]},
  description = 'digitrecklib library provide easy and convenient way to connect to digitreck servers for efficient device location based services.It enables using digiTreck APIs as methods alongwith header and checksum management.',
  author = 'Dheeraj Agrawal',
  author_email = 'dheeraj.agrawal@digitreck.com',
  url = 'https://github.com/digitreck/digitreck-python',
  download_url = 'https://github.com/digitreck/digitreck-python',
  keywords = ["framework", "location", "maps", "maps", "gps", "digitreck", "assests tracking"],
  classifiers = []
)