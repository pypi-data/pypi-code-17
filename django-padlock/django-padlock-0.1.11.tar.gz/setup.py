import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
# README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-padlock',
    version='0.1.11',
    packages=['padlock'],
    description='Middleware Class for add more security on web sessions',
    # long_description=README,
    author='Yelson Chevarrias',
    author_email='chevarrias@gmail.com',
    url='https://github.com/ccapudev/django-padlock/',
    license='GNU General Public License v3.0',
    install_requires=[
        'Django>=1.9,<=1.11',
    ]
)