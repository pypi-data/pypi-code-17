from distutils.core import setup
setup(
  name = 'prosodic',
  packages = ['prosodic'], # this must be the same as the name above
  version = '1.1',
  description = 'PROSODIC: a metrical-phonological parser, written in Python. For English and Finnish, with flexible language support.',
  author = 'Ryan Heuser, Josh Falk, Arto Anttila',
  author_email = 'heuser@stanford.edu',
  url = 'https://github.com/quadrismegistus/prosodic', # use the URL to the github repo
  download_url = 'https://github.com/quadrismegistus/prosodic/archive/1.1.tar.gz', # I'll explain this in a second
  keywords = ['metrical-parser', 'linguistics', 'nlp', 'finnish-language-analysis', 'poetry', 'rhythm'], # arbitrary keywords
  classifiers = [],
)
