from setuptools import setup, find_packages

setup(
    name='Statistical_Computation',
    version='1.3',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Implementation of scalable k-means++',
    install_requires=['numpy'],
    url='https://github.com/susancherry/Statistical_Computation.git',
    author='Susan Cherry',
    author_email='susan.cherry@duke.edu'
)
