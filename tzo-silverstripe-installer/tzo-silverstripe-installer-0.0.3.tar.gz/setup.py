import os
from setuptools import find_packages, setup

base = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(base, 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='tzo-silverstripe-installer',
    version='0.0.3',
    description='Automation script to create new Silverstripe site.',
    long_description=README,
    url='http://git.timezoneone.com/timezoneone/tzo-silverstripe-installer',
    author='Shawn Lin',
    author_email='shawn@timezoneone.com',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    keywords='timezoneone tzo silverstripe',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'tzo-create=silverstripe_installer.silverstripeinstaller:main'
        ],
    }
)
