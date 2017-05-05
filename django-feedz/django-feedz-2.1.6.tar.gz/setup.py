from __future__ import print_function
import os

from setuptools import setup, find_packages

import feedz

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

def get_reqs(*fns):
    lst = []
    for fn in fns:
        for package in open(os.path.join(CURRENT_DIR, fn)).readlines():
            package = package.strip()
            if not package:
                continue
            lst.append(package.strip())
    return lst

setup(
    name="django-feedz",
    version=feedz.__version__,
    packages=find_packages(),
    package_data={
        '': ['docs/*.txt', 'docs/*.py'],
        'feedz': [
#             'static/*/*/*.*',
#             'templates/*.*',
#             'templates/*/*.*',
#             'templates/*/*/*.*',
#             'templates/*/*/*/*.*',
#             'fixtures/*',
            'tests/data/*',
        ],
    },
    author="Chris Spencer",
    author_email="chrisspen@gmail.com",
    description="A Django model for analyzing RSS/Atom feeds.",
    license="BSD",
    url="https://github.com/chrisspen/django-feedz",
    #https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        #'Development Status :: 6 - Mature',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
    ],
    zip_safe=False,
    install_requires=get_reqs('requirements-min-django.txt', 'requirements.txt'),
    tests_require=get_reqs('requirements-test.txt'),
)
