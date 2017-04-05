from setuptools import setup
setup(name='nlplib',
      version='0.0.1',
      url='https://github.com/td391/nlplib',
      author='td391',
      author_email='td39@gmx.com',
      license='MIT',
      platforms='any',
      description='Python client library for langid',
      install_requires=['langid'],
      extras_require={
        'test': ['pytest'],
      },
      packages=['nlplib'])
