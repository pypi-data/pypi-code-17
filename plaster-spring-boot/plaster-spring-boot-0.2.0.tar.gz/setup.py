# Always prefer setuptools over distutils
from codecs import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

execfile('src/data/version.py')

setup(
    name='plaster-spring-boot',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.2.0',
    packages=find_packages(),
    py_modules=[
        'src.plaster',
    ],

    description='Generates scaffolding for new models for Spring Boot projects',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/JDrost1818/plaster',

    # Author details
    author='Jake Drost',
    author_email='JDrost1818@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
    ],

    # What does your project relate to?
    keywords='sample setuptools development',
    install_requires=['pattern', 'pyyaml'],
    entry_points={
        'console_scripts': [
            'plaster = src.plaster:main',
        ]
    }
)
