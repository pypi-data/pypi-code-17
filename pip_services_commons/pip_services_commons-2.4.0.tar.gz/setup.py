"""
Pip.Services Commons
--------------------

Pip.Services is an open-source library of basic microservices.
pip_services_commons package provides basic abstractions portable across variety of languages.

Links
`````

* `website <http://github.com/pip-services/pip-services>`
* `development version <http://github.com/pip-services/pip-services-commons-python>`

"""

from setuptools import setup
from setuptools import find_packages

setup(
    name='pip_services_commons',
    version='2.4.0',
    url='http://github.com/pip-services/pip-services-commons-python',
    license='MIT',
    description='Basic portable abstractions for Pip.Services in Python',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    long_description=__doc__,
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'iso8601', 'PyYAML', 'pystache'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]    
)
