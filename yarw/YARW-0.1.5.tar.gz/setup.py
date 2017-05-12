import os
import versioneer

from setuptools import setup, find_packages

setup(
    name='YARW',
    version=versioneer.get_version(),
    description='Yet Another Registry Wrapper',
    author='Mars Galactic',
    author_email='xoviat@users.noreply.github.com',
    url='https://github.com/xoviat/subzero',
    packages=find_packages(),
    license=open(
        os.path.join(os.path.dirname(__file__), 'LICENSE')).readline().strip(),
    platforms='any',
    keywords=[],
    classifiers=[],
    install_requires=[],
    cmdclass=versioneer.get_cmdclass(),
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md')