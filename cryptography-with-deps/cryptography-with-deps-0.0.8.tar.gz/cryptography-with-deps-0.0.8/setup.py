#!/usr/bin/env python
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        # TODO(snormore): Assuming Ubuntu for now...
        cmd = 'apt-get install -y --force-yes build-essential libssl-dev libffi-dev'
        print('Running command: %s' % (cmd, ))
        output = subprocess.check_output(cmd, shell=True)
        raise ValueError(cmd, output)
        install.run(self)


setup(
    name='cryptography-with-deps',
    version='0.0.8',
    description='Cryptography package that also installs system dependencies.',
    author='Steven Normore',
    author_email='steven@dataup.io',
    url='https://dataup.io/',
    packages=find_packages(),
    scripts=[],
    install_requires=[
        'cryptography'
    ],
    cmdclass={
        'install': CustomInstallCommand,
    }
)
