from __future__ import print_function
from __future__ import division

from setuptools import setup, find_packages
from pip.req import parse_requirements

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    _license = f.read()

install_requirements = parse_requirements('requirements.txt', session=False)
requirements = [str(ir.req) for ir in install_requirements]

setup(
    name='s3-uploader',
    version='0.0.2',
    description='Command line tool for uploading resources to S3',
    long_description=readme,
    author='Onfido',
    url='https://github.com/onfido/s3-uploader/',
    license=_license,
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            's3-uploader = s3_uploader.main:main', ], },
    keywords=['python', 's3', 'aws', 'upload', 'binaries', 'resources',
              'boto3', 'uploader'],
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
