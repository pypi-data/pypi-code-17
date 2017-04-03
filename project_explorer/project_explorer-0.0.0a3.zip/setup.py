
from setuptools import setup

setup(
    name='project_explorer',
    version='0.0.0a3',
    description='A simple file browser that uses project based concepts.',
    url='https://github.com/mfish38/project_explorer',
    author='Mark Fisher',
    license='MIT',
    packages=['project_explorer'],
    install_requires=[
        'PySide',
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Topic :: Desktop Environment :: File Managers',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
    ]
)
