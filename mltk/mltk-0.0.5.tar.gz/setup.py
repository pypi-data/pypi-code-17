from distutils.core import setup
requirements = ["numpy", "pandas"]

setup(
  name = 'mltk',
  packages = ['mltk', 'mltk.metrics', 'mltk.visualization'], # this must be the same as the name above
  version = '0.0.5',
  description = 'Machine learning toolkit for python',
  author = 'Manan Shah',
  author_email = 'manan.shah.777@gmail.com',
  url = 'https://github.com/mananshah99/mltk', # use the URL to the github repo
  keywords = ['ml', 'metrics', 'toolkit'], # arbitrary keywords
  install_requires = requirements,
  classifiers = [],
)
