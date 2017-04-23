from distutils.core import setup
setup(
  name = 'prosodic',
  packages = ['prosodic','prosodic/lib','prosodic/lib/feats','prosodic/metricaltree','prosodic/dicts','prosodic/dicts/en','prosodic/dicts/en/pyphen','prosodic/dicts/fi','prosodic/dicts/fi/syllabifier','prosodic/meters'], # this must be the same as the name above
  version = '1.1.7',
  description = 'PROSODIC: a metrical-phonological parser, written in Python. For English and Finnish, with flexible language support.',
  author = 'Ryan Heuser, Josh Falk, Arto Anttila',
  author_email = 'heuser@stanford.edu',
  url = 'https://github.com/quadrismegistus/prosodic', # use the URL to the github repo
  download_url = 'https://github.com/quadrismegistus/prosodic/archive/1.1.tar.gz', # I'll explain this in a second
  keywords = ['metrical-parser', 'linguistics', 'nlp', 'finnish-language-analysis', 'poetry', 'rhythm'], # arbitrary keywords
  classifiers = [],
  install_requires=['numpy','nltk'],
  package_data={
        'prosodic': ['corpora/**/*.txt', 'dicts/**/*.tsv','dicts/**/*.txt','dicts/en/pyphen/dictionaries/*.dic','dicts/fi/syllabifier/*.txt','metricaltree/*.sh', 'metricaltree/*.md','tagged_samples/*.txt']
    },
    #recursive-include corpora *.txt
    #recursive-include dicts *.txt *.sh *.md *.tsv
    #recursive-include metricaltree *.sh *.md
    #recursive-include tagged_samples *.txt

)
