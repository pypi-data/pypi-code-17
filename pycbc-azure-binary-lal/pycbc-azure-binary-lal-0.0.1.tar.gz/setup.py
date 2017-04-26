from distutils.core import setup

setup(name='pycbc-azure-binary-lal',
      version='0.0.1',
      description='some shared object files from lalsuite, no gaurantees',
      author='Alex Nitz',
      author_email='alex.nitz@aei.mpg.de',
      packages=['lal', 'lalsimulation', 'lalframe', 'blal'],
     )
