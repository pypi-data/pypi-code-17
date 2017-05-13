from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='howlermonkey',
    version='1.0.2',
    packages=['howlermonkey'],
    url='https://gitlab.dtg.cl.cam.ac.uk/infrastructure/howler-monkey/',
    license='MIT',
    author='Thomas Bytheway',
    author_email='thomas.bytheway@cl.cam.ac.uk',
    description='A slack messaging authentication and'
                'interfacing system for the DTG',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'],
    install_requires=['requests>=2.10.0', 'pyyaml>=3.11']
)
