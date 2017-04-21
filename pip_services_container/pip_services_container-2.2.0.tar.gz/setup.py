"""
Pip.Services Container
----------------------

Pip.Services is an open-source library of basic microservices.
pip_services_container provides IoC container implementation.

Links
`````

* `website <http://www.pipservices.org>`_
* `development version <http://github.com/pip-services/pip-services-container-python>`

"""

from setuptools import setup
from setuptools import find_packages

setup(
    name='pip_services_container',
    version='2.2.0',
    url='http://github.com/pip-services/pip-services-container-python',
    license='MIT',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    description='IoC container for Pip.Services in Python',
    long_description=__doc__,
    packages=find_packages(exclude=['config', 'data', 'examples', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'iso8601', 'PyYAML', 'pip_services_commons'
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
