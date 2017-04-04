from setuptools import find_packages, setup

__version__ = '0.9.0a1'

setup(
    name='pyrunscope',
    version=__version__,
    packages=find_packages(),
    install_requires=['restkit'],
    url='http://github.com/drewsonne/pyrunscope',
    license='LGPLv2',
    author='Drew J. Sonne',
    author_email='drew.sonne@gmail.com',
    description='',
    include_package_data=True
)
