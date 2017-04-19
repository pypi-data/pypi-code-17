from setuptools import setup, find_packages
from codecs import open
from os import path

root = path.abspath(path.dirname(__file__))

with open(path.join(root, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='jaeum-modifier',
    version='0.0.1a0',

    description='Hangul Jaeum Modifier',
    long_description=long_description,

    url='https://github.com/hyunchel/jaeum-modifier',

    author='Hyunchel Kim',
    author_email='hyunchel.inbox@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 1 - Planning',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing :: Linguistic',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
    ],

    keywords='language hangul jaeum modify',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    py_modules=['jaeum-modifier'],

    install_requires=['hangulize<=0.0.7'],
)

