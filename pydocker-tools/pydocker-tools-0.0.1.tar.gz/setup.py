from setuptools import setup, find_packages

readme = open('README.rst').read()
changes = open('CHANGES.rst').read()

setup(
    name='pydocker-tools',
    version='0.0.1',
    description='pydocker-tools is a set of tools to work around lengthy or piped command line tools for docker',
    license='MIT',
    url='https://github.com/jojees/pydocker-tools',
    author='Joji Vithayathil Johny',
    author_email='joji@jojees.net',
    long_description=readme + '\n\n' + changes,

    packages=find_packages(
        exclude=['tests']
    ),

    test_suite='tests',

    entry_points={
        'console_scripts': [
            'jpy-dtools = pydockertools.jpydtools:main'
        ]
    },
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Shells',
        'Topic :: System :: Systems Administration',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Utilities'
    ],
    
    keywords='additional docker commandline tools'
)
