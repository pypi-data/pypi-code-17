from setuptools import setup, find_packages
import os

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
with open('requirements.txt') as requirements:
    install_requires = requirements.read().splitlines()

import io
with io.open('README.md', encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='BBB-LCDDisplay',
    version='1.0.16',
    packages=find_packages(),
    install_requires=install_requires,
    author="Petit Jonathan, William De Decker, William Chagnot",
    author_email="petit.jonathan16@gmail.com",
    description="Gpio, i2c, Pwm for Beaglebone black",
    long_description= long_description,
    include_package_data=True,
    url='https://github.com/JonathanPetit/BBB-LCDDisplay',
    license= 'MIT',
    keywords = 'Beaglebone black',
    classifiers=[
        "Programming Language :: Python",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
    ],
)
