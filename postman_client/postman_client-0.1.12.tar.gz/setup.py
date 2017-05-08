# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='postman_client',
    version='0.1.12',
    install_requires=[
        'requests==2.11.0',
        'simplejson==3.6.4',
        'apysignature==0.1.3'
    ],
    url='https://github.com/ThCC/postman-client',
    description='Client service, to send simple text emails or, using a template created at Postman, send more complex emails.',
    long_description=open("README.rst").read(),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries',
    ],
    author='Thiago Cardoso de Castro',
    author_email='thiago.decastro2@gmail.com',
)
