from setuptools import setup  # type: ignore

# pip doesn't have a `tests_require`, but we only need these for testing
# https://github.com/pypa/pip/issues/1197
tests_require = ['mock', 'PyJwt']

setup(
    name='edpanalyst',
    packages=['edpanalyst'],
    version='0.0.15',
    description='The python API to the Empirical Data Platform.',
    license='Apache License 2.0',
    # TODO(asilvers): This scipy dep is gross and only because we're running
    # guess client-side. Kill it when guess moves server-side.
    install_requires=[
        'configparser', 'future', 'matplotlib', 'pandas', 'requests',
        'scipy', 'seaborn', 'tqdm', 'typing', 'enum34'] + tests_require
)
