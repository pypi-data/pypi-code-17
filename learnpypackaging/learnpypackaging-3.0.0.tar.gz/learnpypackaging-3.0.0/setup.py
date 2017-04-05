from setuptools import setup


__VERSION__ = '3.0.0'


setup(
    name="learnpypackaging",
    version=__VERSION__,
    package_data={
        'learnpypackaging': ['data/*.html'],
    },
)
