from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.breadcrumbs'
version = '0.2.1'
readme = open(join('src', 'dolmen', 'breadcrumbs', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'cromlech.i18n',
    'cromlech.browser >= 0.5',
    'dolmen.location >= 0.2',
    'dolmen.template >= 0.2',
    'setuptools',
    'zope.interface',
    ]

tests_require = [
    'cromlech.browser [test]',
    'zope.location',
    ]

setup(name = name,
      version = version,
      description = 'Breadcrumbs navigation for the Cromlech framework.',
      long_description = readme + '\n\n' + history,
      keywords = 'Cromlech Dolmen',
      author = 'Souheil Chelfouh',
      author_email = 'trollfot@gmail.com',
      url = 'http://gitweb.dolmen-project.org',
      download_url = '',
      license = 'ZPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages = ['dolmen'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      tests_require = tests_require,
      install_requires = install_requires,
      extras_require = {'test': tests_require},
      classifiers = [
          'Environment :: Web Environment',
          'Intended Audience :: Other Audience',
          'License :: OSI Approved :: Zope Public License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          ],
      )
