from setuptools import setup
setup(
    name='signaler',
    packages=['signaler'],
    version='0.0.1',
    description=('Simple signal handling'),
    install_requires=[
        'six'
    ],
    author='Guy Hughes',
    author_email='g@gxg.me',
    url='https://github.com/guyhughes/signaler',
    keywords=['signal','sigint'],
    license='MPL 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
    ]
)
