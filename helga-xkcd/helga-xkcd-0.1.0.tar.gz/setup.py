from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    'helga',
    'requests'
]

EXTRAS_REQUIRE = {
    'development': ['ipython<6.0', 'twine', 'wheel'],
    'testing': ['pytest', 'tox'],
}

setup(
    name='helga-xkcd',
    version='0.1.0',
    description='A helga plugin to fetch xkcd comics',

    author='Cameron Lane',
    author_email='crlane@adamanteus.com',
    url='https://github.com/crlane/helga-xkcd',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=True,
    entry_points=dict(
        helga_plugins=[
            'xkcd=helga_xkcd.command:xkcd',
        ],
    ),
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
        'Framework :: Twisted',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
