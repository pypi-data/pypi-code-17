from distutils.core import setup

setup(
    name='prax',
    version='0.1.0.1',
    packages=[''],
    url='https://github.com/Jake-R/prax/archive/0.1.0.1.tar.gz',
    license='MIT License',
    author='robie',
    author_email='jacob.robie@gmail.com',
    description='A data conversion utility',
    entry_points={
        'console_scripts': [
            'prax = prax:main'
        ]
    }
)
