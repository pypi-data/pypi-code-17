import textwrap
import versioneer

from setuptools import find_packages, setup

setup(
    name='win32compat',
    version=versioneer.get_version(),
    description='Python for Window Extensions',
    long_description=textwrap.dedent('''
        Python extensions for Microsoft Windows'
        Provides access to much of the Win32 API, the
        ability to create and use COM objects, and the
        Pythonwin environment
        
        This provides backward compatibility.
        '''),
    author='Mark Hammond (et al)',
    author_email='mhammond@users.sourceforge.net',
    url='http://sourceforge.net/projects/pywin32/',
    license='GNU GPL v3',
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages())
