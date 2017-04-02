from distutils.core import setup
setup(
  name = 'NautilusPy',
  packages = ['NautilusPy'], # this must be the same as the name above
  version = '1.0.0',
  package_data={'NautilusPy': ['core/*.py', "*.py"]},
  description = 'Nautilus library provide easy and convenient way to connect to nautilus servers.',
  author = 'Dheeraj Agrawal',
  author_email = 'dheeraj.agrawal@digitreck.com',
  url = 'https://github.com/digitreck/nautilus-py', # use the URL to the github repo
  download_url = 'https://github.com/digitreck/nautilus-py', # I'll explain this in a second
  keywords = ["framework", "location", "maps", "tracking", "gps", "digitreck", "assests tracking"], # arbitrary keywords
  classifiers = []
)