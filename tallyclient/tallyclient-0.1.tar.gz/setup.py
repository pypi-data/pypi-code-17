from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='tallyclient',
      version='0.1',
      description='Python client for go-tally server',
      long_description=readme(),
      url='https://github.com/phouse512/tally-client',
      author='phouse512',
      author_email='phouse512@gmail.com',
      license='MIT',
      packages=['tallyclient'],
      zip_safe=False)

