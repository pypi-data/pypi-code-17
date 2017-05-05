"""Setup script for the Logga project.
"""
import setuptools


PACKAGES = [
    'pylint',
    'sphinx_rtd_theme==0.1.10a0',
    'twine',
    'Sphinx==1.4.5',
]

SETUP_KWARGS = {
    'name': 'logga',
    'version': '1.0.1',
    'description': 'Python standard log wrapper, with added goodness',
    'author': 'Lou Markovski',
    'author_email': 'lou.markovski@gmail.com',
    'url': 'https://github.com/loum/logga',
    'install_requires': PACKAGES,
    'packages': setuptools.find_packages(),
    'package_data': {
        'logga': [
        ],
    },
    'license': 'MIT',
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
}

setuptools.setup(**SETUP_KWARGS)
