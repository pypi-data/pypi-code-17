from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='generalized_blender',
    
    url='https://github.com/Pradeep3490/Blender_Package',
    author='Pradeep Jeyachandran',
    author_email ="charmofsilence@gmail.com",
    description='Python implementation of generalized model blender with K fold CV',
    packages=['generalized_blender'],
    install_requires=['numpy', 'scipy','scikit_-learn'],
)
