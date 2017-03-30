from distutils.core import setup
setup(
  name = 'YAPyOrg',
  packages = ['YAPyOrg'], # this must be the same as the name above
  version = '0.1',
  description = 'Yet Another Python parsing library',
  author = 'Stefan Nožinić',
  author_email = 'stefan@lugons.org',
  url = 'https://github.com/fantastic001/yapyorg', # use the URL to the github repo
  download_url = 'https://github.com/fantastic001/yapyorg/tarballs/0.1', 
  keywords = ['org-mode', 'parsing', 'emacs'],
  package_dir = {'YAPyOrg': 'src/lib'},
  classifiers = [],
)
