from setuptools import (setup,
                        find_packages)

setup(name='cassandra_helpers',
      packages=find_packages(),
      version='0.0.0',
      description='Helper functions for comfortable working with cassandra-driver.',
      author='Azat Ibrakov',
      author_email='azatibrakov@gmail.com',
      url='https://github.com/lycantropos/cassandra_helpers',
      download_url='https://github.com/lycantropos/cassandra_helpers/archive/'
                   'master.tar.gz',
      keywords=['Cassandra'],
      install_requires=['cassandra-driver>=3.9.0'])
