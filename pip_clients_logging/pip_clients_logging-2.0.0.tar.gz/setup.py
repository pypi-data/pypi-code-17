"""
Pip.Services Logging Client
-----------------------------

Python client to pip_services_logging microservice

Links
`````

* `website <http://github.com/pip-services/pip-services>`
* `development version <http://github.com/pip-services-infrastructure/pip-clients-logging-python>`

"""

from setuptools import setup
from setuptools import find_packages

setup(
    name='pip_clients_logging',
    version='2.0.0',
    url='http://github.com/pip-services-infrastructure/pip-clients-logging-python',
    license='MIT',
    description='Python client to pip-services-logging microservice',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    long_description=__doc__,
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'iso8601', 'PyYAML', 'bottle', 'requests',
        'pip_services_commons', 'pip_services_net'
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
