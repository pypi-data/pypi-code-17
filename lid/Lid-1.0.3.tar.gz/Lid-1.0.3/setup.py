import os
from setuptools import setup,find_packages

with open(os.path.abspath('.')+'/VERSION', 'r') as line:
    version = line.readline()

setup(
    name = 'Lid',
    version = version,
    description = 'tiny project',
    keywords = ["lid", "python3"],
    author = 'zouhao',
    author_email = 'hellworld.zouhao@gmail.com',
    maintainer = 'zouhao',
    maintainer_email = 'helloworld.zouhao@gmail.com',
    url = 'http://blog.owlsn.com',
    license = 'MIT License',
    platforms = ['any'],
    classifiers = [
        'Development Status :: 1 - Planning'
    ],
    packages = find_packages()
)