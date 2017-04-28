from setuptools.command.install import install
from distutils.core import setup


class PybluezInstall(install):
    """
    Custom install script to install pybluez locally on a linux machine
    """
    def run(self):
        # handle the super install
        install.run(self)

setup(
    name='villagereach',
    version='0.0.2',
    author='D4D',
    author_email='leohentschker@college.harvard.edu',
    packages=['villagereach', 'villagereach.test'],
    scripts=[],
    url='http://pypi.python.org/pypi/VillageReach/',
    license='LICENSE.txt',
    description='Facilitating bluetooth file transfer',
    long_description=open('README.txt').read(),
    install_requires=[],
    cmdclass={"install": PybluezInstall}
)
