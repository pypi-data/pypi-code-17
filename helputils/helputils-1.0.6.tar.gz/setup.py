from distutils.core import setup
from setuptools import find_packages

setup(
    name="helputils",
    version="1.0.6",
    author="eayin2",
    author_email="eayin2@gmail.com",
    packages=find_packages(),
    url="https://github.com/eayin2/helputils",
    description="Bunch of random useful functions and classes",
    install_requires=["gymail", "pymongo", "Pillow"],
)
