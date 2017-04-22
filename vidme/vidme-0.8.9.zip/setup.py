from distutils.core import setup

setup(
  name = 'vidme',
  packages = ['vidme'], # this must be the same as the name above
  version = '0.8.9',
  description = 'This is a Python VidMe API interface library.',
  author = 'KingFredrickVI',
  author_email = 'jakewright458@gmail.com',
  url = 'https://github.com/KingFredrickVI/VidMeAPI', # use the URL to the github repo
  download_url = 'https://github.com/KingFredrickVI/VidMeAPI/archive/master.zip', # I'll explain this in a second
  keywords = ['vidme', 'VidMe', 'Vid.Me', 'vid.me', 'python', 'api', 'vidme api'], # arbitrary keywords
  classifiers = [],
)

# setup.py sdist upload -r pypi
