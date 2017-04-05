from setuptools import setup

__VERSION__ = '1.12.5'

setup(
    name="learnpypackaging",
    version=__VERSION__,
    package_data={
        'learnpypackaging': ['data/*.html'],
    },
)
