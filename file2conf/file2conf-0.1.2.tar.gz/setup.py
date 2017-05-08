from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
version = '0.1.2'
modules = ['PyYAML', 'ujson']

setup(
    name='file2conf',
    version=version,
    description='Lib for reading configs',
    long_description='Lib for reading configs',
    author='KTS',
    author_email='file2conf@ktsstudio.ru',
    url='https://github.com/KTSStudio/confman',
    download_url='https://github.com/KTSStudio/confman/tarball/' + version,
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords=' '.join(['configs', 'yaml', 'json', 'python']),
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=modules,
)
