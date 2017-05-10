try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='BOASM',
      version='00.01.00',
      description='Budgeted Online Active Surrogate Modeling',
      long_description=('Budgeted Online Active Surrogate Modeling'),
      url='https://boasm.github.io/',
      license='CC BY-NC-SA 4.0',
      author='Amir Sani',
      author_email='reachme@amirsani.com',
      packages=['boasm'],
      )
