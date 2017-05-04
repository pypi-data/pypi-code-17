from setuptools import setup

setup(
    name='pylint-ci',
    version='1.0.0',
    packages=['pylint_ci'],
    install_requires=['pylint'],
    entry_points={
        'console_scripts': ['pylint-ci = pylint_ci.__main__:main'],
    },
)
