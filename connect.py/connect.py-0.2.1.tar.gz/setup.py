from setuptools import setup, find_packages
import re

with open('requirements.txt') as f:
    requirements = f.readlines()

with open('connect/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open('README.md') as f:
    readme = f.read()

setup(name='connect.py',
      author='GiovanniMCMXCIX',
      url='https://github.com/GiovanniMCMXCIX/connect.py',
      version=version,
      packages=find_packages(),
      license='MIT',
      description='An API wrapper for Monstercat Connect written in Python.',
      long_description=readme,
      include_package_data=True,
      install_requires=requirements,
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Internet',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
      ]
      )
