from distutils.core import setup

setup(
    name='prax',
    version='0.1.1.2',
    packages=[],
    url='https://github.com/Jake-R/prax',
    license='MIT License',
    author='robie',
    author_email='jacob.robie@gmail.com',
    description='A data conversion utility',
    entry_points={
        'console_scripts': [
            'prax = prax:main'
        ]
    },
    install_requires=['grako', 'future']
)
