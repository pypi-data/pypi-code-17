from setuptools import setup, find_packages


setup(
        name='serialstruct',
        version='1.0.22',
        description=('Implements a StructuredPacket for pySerial\'s '
            'serial.threaded module'),
        long_description='long description',
        author='Eric Oswald',
        author_email='eoswald39@gmail.com',
        url='https://github.com/eoswald/serialstruct',
        license='MIT',
        packages=find_packages(exclude=['test']),
        install_requires=['pyserial']
)
