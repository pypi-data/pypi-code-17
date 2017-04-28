import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-padlock',
    version='0.1.7.12',
    packages=['padlock'],
    description='Middleware Class for add more security on web sessions',
    long_description=README,
    author='Yelson Chevarrias (CcapuDev)',
    author_email='chevarrias@gmail.com',
    url='https://github.com/ccapudev/django-padlock/',
    license='GNU General Public License v3.0',
    platform='Linux OS',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
    install_requires=[
        'Django>=1.7,<1.11',
    ]
)