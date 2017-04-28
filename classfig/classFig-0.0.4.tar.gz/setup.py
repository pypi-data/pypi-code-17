# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
setup(
    name="classFig",
    version="0.0.4",
    packages=find_packages(),
    scripts=['classFig.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
#    install_requires=['docutils>=0.3'],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },
        
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],
    
    install_requires=[
          'matplotlib',
          'cycler',
      ],

    # metadata for upload to PyPI
    author="Fabolu",
    author_email="fabolu@posteo.de",
    description="Comfortable figure handling in Python3 / Matplotlib",
    license="MIT",
    keywords="classFig matplotlib",
    url="https://github.com/Fabolu/classFig",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)