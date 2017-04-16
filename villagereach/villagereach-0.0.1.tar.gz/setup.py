from setuptools.command.install import install
from distutils.core import setup


class PybluezInstall(install):
    def run(self):
        install.run(self)

setup(
    name='villagereach',
    version='0.0.1',
    author='D4D',
    author_email='leohentschker@college.harvard.edu',
    packages=['villagereach', 'villagereach.test'],
    scripts=[],
    url='http://pypi.python.org/pypi/VillageReach/',
    license='LICENSE.txt',
    description='Facilitating file transfer between drones and basis',
    long_description=open('README.txt').read(),
    install_requires=[],
    cmdclass={"install": PybluezInstall}
)
