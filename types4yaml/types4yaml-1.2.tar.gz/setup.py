from setuptools import setup, find_packages

setup(
    name='types4yaml',
    version='1.2',
    packages=find_packages(),
    install_requires=['docopt', 'PyYAML'],

    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',

    entry_points={
        'console_scripts': [
            'yamlint = types4yaml.check:main'
        ]
    },

    author='Thomas Conway',
    author_email='drtomc@gmail.com',
    description='A basic type schema for JSON/YAML data'
)
