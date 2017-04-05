from setuptools import setup


__VERSION__ = '3.0.1'


setup(
    name="learnpypackaging",
    version=__VERSION__,
    package_data={
        'learnpypackaging': ['data/*.html'],
    },
    packages=['learnpypackaging'],
)
