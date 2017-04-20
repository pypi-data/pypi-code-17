"""

"""

__author__ = 'Thomas Li Fredriksen'
__license__ = 'MIT'

import setuptools
from distutils.core import setup
from os import path

PWD = path.abspath(path.dirname(__file__))
README_PATH=path.join(PWD, 'README.md')

### Generate description
try:
    import pypandoc
    long_description = pypandoc.convert(README_PATH, 'rst')
except(IOError, ImportError):
    print '***Failed to import pypandoc. Displaying unformatted markdown***'

    from codecs import open
    with open(README_PATH, encoding='utf-8') as f:
        long_description = f.read()

data = dict(
        name='NeoPySwitch',
        version='0.2.0',
        url='https://github.com/thomafred/NeoPySwitch',
        packages=['NeoPySwitch'],
        package_data={
            'NeoPySwitch' : [
                'LICENSE',
                'README.md'
                ]
            },
        license='MIT',
        description='Python switch implementation',
        long_description=long_description,
        provides=['NeoPySwitch'],
        install_requires=[],
        author='Thomas Li Fredriksen',
        author_email='tom@lifredriksen.no',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Topic :: Software Development',
            'Programming Language :: Python :: 2.4',
            'Programming Language :: Python :: 2.5',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            ],
        )

if __name__ == '__main__':
    setup(**data)
