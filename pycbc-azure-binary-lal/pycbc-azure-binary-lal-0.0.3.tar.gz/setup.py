from setuptools import setup

setup(name='pycbc-azure-binary-lal',
      version='0.0.3',
      description='some shared object files from lalsuite, no gaurantees',
      author='Alex Nitz',
      author_email='alex.nitz@aei.mpg.de',
      install_requires=['pycbc'],
      package_data={'blal': ['*.so*']},
      packages=['lal', 'lalsimulation', 'lalframe', 'blal'],
     )
