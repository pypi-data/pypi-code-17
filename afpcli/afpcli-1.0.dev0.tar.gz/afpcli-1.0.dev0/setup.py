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
        name = 'afpcli',
        version = '1.0.dev0',
        description = 'Placeholder for afp-cli in case someone misspells it',
        long_description = "This package exists so that people can misspell 'afp-cli' as 'afpcli' and still get what they expect.",
        author = '',
        author_email = '',
        license = '',
        url = '',
        scripts = [],
        packages = ['afpcli'],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = ['afp-cli'],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = [],
    )
