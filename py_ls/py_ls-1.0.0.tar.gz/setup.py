from setuptools import setup, find_packages

setup(
    name='py_ls',
    version='1.0.0',
    description='Python likes scala',
    author_email='szalapski.pawel@gmail.com',
    author='Pawel Szalapski',
    url='https://github.com/Szala---/pyls',
    packages=find_packages(exclude=('tests',))
)
