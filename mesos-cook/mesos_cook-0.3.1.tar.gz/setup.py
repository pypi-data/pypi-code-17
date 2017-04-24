from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


def version():
    from mesos_cook.__version__ import __version__
    return __version__


setup(
    name='mesos_cook',
    version=version(),
    description="Python client for Two Sigma's Cook scheduler",
    long_description=readme(),
    url='https://github.com/roguePanda/mesos_cook',
    author='Ben Navetta',
    author_email='benjamin_navetta@brown.edu',
    license='MIT',
    packages=['mesos_cook'],
    install_requires=['requests>=2.13.0', 'six>=1.10.0', 'docopt>=0.6.2', 'pystachio>=0.8.3', 'Cerberus>=1.1', 'terminaltables>=3.1.0'],
    entry_points={
        'console_scripts': ['cook=mesos_cook.cli:main']
    },
    zip_safe=True
)
