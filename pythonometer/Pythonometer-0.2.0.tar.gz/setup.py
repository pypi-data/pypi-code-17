
from setuptools import setup, find_packages

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='Pythonometer',
    version='0.2.0',
    description='A tool for measuring and improving Python skills',
    long_description=long_description,
    url='https://github.com/samuelfekete/Pythonometer',
    author='Samuel Fekete',
    packages=find_packages(),
    scripts=['native_app.py'],
    entry_points={
        'console_scripts': [
            'pythonometer=native_app:main'
        ]
    }
)
