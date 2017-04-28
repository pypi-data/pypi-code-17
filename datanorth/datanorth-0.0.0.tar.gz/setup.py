import sys
import re
from setuptools import setup, find_packages


def get_version():
    with open('datanorth/version.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')


def readme():
    ''' Returns README.rst contents as str '''
    with open('README.rst') as f:
        return f.read()

install_requires = [
    'requests'
]

lint_requires = [
    'pep8',
    'pyflakes'
]

tests_require = [
    'pytest'
]
dependency_links = []
setup_requires = ['pytest-runner']
extras_require = {
    'test': tests_require,
    'all': install_requires + tests_require,
    'docs': ['sphinx'] + tests_require,
    'lint': lint_requires
}

setup(
    name='datanorth',
    version=get_version(),
    description='Python client for the DataNorth API.',
    long_description=readme(),
    author='Jason Haas',
    author_email='jasonrhaas@gmail.com',
    license='MIT',
    url='https://github.com/data-north/datanorth-python',
    keywords=['datanorth', 'api', 'python'],
    packages=['datanorth'],
    package_data={},
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=setup_requires,
    extras_require=extras_require,
    dependency_links=dependency_links,
    zip_safe=True,
    include_package_data=True,
)
