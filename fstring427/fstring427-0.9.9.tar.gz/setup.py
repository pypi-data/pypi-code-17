from setuptools import setup, find_packages
from codecs import open

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='fstring427',
    version='0.9.9',
    description='Python 3.6 f-string sympathy for  Python 2.7. Now with printf()',
    long_description=read_md('README.md'),
    url='https://github.com/smartvid-io/fstring427',
    author='Sean True',
    author_email='strue@smartvid.io',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='programmer productivity',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[],
)