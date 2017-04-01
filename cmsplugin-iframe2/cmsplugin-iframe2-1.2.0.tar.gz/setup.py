# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name            = 'cmsplugin-iframe2',
    version         = '1.2.0',
    description     = 'Customizable Django CMS plugin for including iframes',
    author          = 'Jakub Dorňák',
    author_email    = 'jakub.dornak@misli.cz',
    license         = 'BSD',
    url             = 'https://github.com/misli/cmsplugin-iframe2',
    packages        = find_packages(),
    include_package_data = True,
    install_requires = [
        'django-cms',
    ],
    classifiers     = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Czech',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
