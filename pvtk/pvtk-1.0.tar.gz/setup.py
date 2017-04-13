from setuptools import setup

def readme():
    with open('README') as f:
        return f.read()

setup(name = 'pvtk',
      description = 'precipitation verification toolkit',
      long_description = readme(),
      version = '1.0',
      url = 'https://pypi.python.org/pypi/pvtk',
      author = 'Fan Han',
      author_email = 'hanfan5598@gmail.com',
      packages = ['pvtk'],
      install_requires=[
          'numpy',
          'scipy',
      ],

      )

