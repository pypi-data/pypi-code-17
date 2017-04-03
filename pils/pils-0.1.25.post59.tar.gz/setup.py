#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'pils',
        version = '0.1.25-59',
        description = '''PILS - Python uTILS''',
        long_description = '''PILS is a container for utilities written in python''',
        author = "",
        author_email = "",
        license = 'Apache License 2.0',
        url = 'https://github.com/ImmobilienScout24/pils',
        scripts = [],
        packages = ['pils'],
        py_modules = [],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = ['boto3'],
        dependency_links = [],
        zip_safe=True,
        cmdclass={'install': install},
    )
