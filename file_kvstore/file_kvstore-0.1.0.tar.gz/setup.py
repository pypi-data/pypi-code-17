from setuptools import find_packages
from setuptools import setup


setup(
    name='file_kvstore',
    version='0.1.0',
    description='Tool for storing key/value pairs in text files',
    author='Michael Christen',
    url='https://github.com/michael-christen/file-kvstore',
    license='MIT',
    packages=find_packages(exclude=["*.tests"]),
    install_requires=[
        'PyYAML',
    ],
    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': ['fkvstore=file_kvstore.parser:main'],
    },
)
