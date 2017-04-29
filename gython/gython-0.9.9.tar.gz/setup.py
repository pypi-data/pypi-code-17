import os
import versioneer

from setuptools import setup, find_packages

setup(
    name='gython',
    version=versioneer.get_version(),
    description='Python to go transpiler',
    author='Mars Galactic',
    author_email='xoviat@users.noreply.github.com',
    url='https://github.com/xoviat/gython',
    packages=find_packages(),
    license=open(os.path.join(os.path.dirname(__file__), 'LICENSE.md'))
    .readline().strip(),
    entry_points={
        'console_scripts': ['gython = gython.__main__:main'],
    },
    platforms='any',
    classifiers=[],
    install_requires=[],
    cmdclass=versioneer.get_cmdclass(),
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md')
