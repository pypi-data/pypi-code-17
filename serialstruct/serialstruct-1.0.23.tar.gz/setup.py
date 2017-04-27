import codecs
from setuptools import setup, find_packages


def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        return f.read()


setup(
        name='serialstruct',
        version='1.0.23',
        description=('Implements a StructuredPacket for pySerial\'s '
            'serial.threaded module'),
        long_description=long_description(),
        author='Eric Oswald',
        author_email='eoswald39@gmail.com',
        url='https://github.com/eoswald/serialstruct',
        license='MIT',
        packages=find_packages(exclude=['test']),
        install_requires=['pyserial']
)
