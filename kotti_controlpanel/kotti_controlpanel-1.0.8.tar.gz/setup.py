import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''
try:
    CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except IOError:
    CHANGES = ''

version = '1.0.8'

install_requires = [
    'Kotti>=1.0.0',
    'unidecode',
    'kotti_pdf>=0.4.2'
]


setup(
    name='kotti_controlpanel',
    version=version,
    description="Settings configuration for Kotti",
    long_description='\n\n'.join([README, CHANGES]),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: Repoze Public License",
    ],
    author='Oshane Bailey',
    author_email='b4.oshany@gmail.com',
    url='https://github.com/b4oshany/kotti_controlpanel',
    keywords='ui settings controlpanel kotti web cms wcms pylons pyramid sqlalchemy bootstrap',
    license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=[],
    dependency_links=[],
    entry_points={
        'fanstatic.libraries': [
            'kotti_controlpanel = kotti_controlpanel.fanstatic:library',
        ],
    },
    package_data={"kotti_controlpanel": ["templates/*", "static/*",
                                          "locale/*", "views/*",
                                          "alembic/*.*",
                                          "alembic/versions/*"]},
    extras_require={},
)
