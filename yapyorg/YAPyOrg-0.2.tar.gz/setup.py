from distutils.core import setup
setup(
  name = 'YAPyOrg',
  packages = ['YAPyOrg'], # this must be the same as the name above
  version = '0.2',
  description = 'Yet Another Python Org-mode parser',
  author = 'Stefan Nožinić',
  author_email = 'stefan@lugons.org',
  url = 'https://github.com/fantastic001/YAPyOrg', # use the URL to the github repo
  download_url = 'https://github.com/fantastic001/YAPyOrg/tarball/0.2', 
  keywords = ['library', 'parsing', 'org-mode'], 
  package_dir = {'YAPyOrg': 'src/lib'},
  classifiers = []
)

