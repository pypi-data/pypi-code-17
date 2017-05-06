from setuptools import (setup,
                        find_packages)

from lovelace.config import PACKAGE

setup(name=PACKAGE,
      version='0.0.1',
      packages=find_packages(),
      install_requires=[
          'aiohttp>=1.3.3',
      ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest>=3.0.5',
                     'pytest-asyncio>=0.5.0',
                     'pytest-cov>=2.4.0',
                     'pydevd>=1.0.0',  # debugging
                     'hypothesis>=3.6.1',
                     ])
