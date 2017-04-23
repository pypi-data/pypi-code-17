from setuptools import setup
setup(
  name = 'pycricket',
  packages = ['pycricket'], 
  version = '0.3',
  description = 'A library for fetching cricket scorecards of past cricket matches',
  author = 'Shivam Mitra',
  author_email = 'shivamm389@gmail.com',
  license = 'GPLv2',
  url = 'https://github.com/codophobia/cricket-scorecards-and-commentary-with-python', 
  download_url = 'https://github.com/codophobia/cricket-scorecards-and-commentary-with-python/tarball/0.2', 
  keywords = ['cricket', 'scorecards'], 
  install_requires=[
          'beautifulsoup4'
      ],
  classifiers = [],
  package_data={
    'pycricket': ['data/*.csv','matches.csv'],
  },
  include_package_data=True,
)

