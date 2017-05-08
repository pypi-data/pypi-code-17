"""
Flask-ConfigHelper
-------------

Helper utility for initializing environment configurations and verifying required config variables are present
"""

from setuptools import setup

setup(
    name='flask-confighelper',
    version='1.0.0',
    url='https://github.com/byt3smith/flask-confighelper',
    license='MIT License',
    author='Bob Argenbright',
    description='Helper for setting up environment configurations',
    long_description=__doc__,
    py_modules=['flask_confighelper'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
