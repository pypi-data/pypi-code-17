import re
import os
from setuptools import setup


PKG = 'mpris_scrobbler'
VERSIONFILE = os.path.join(PKG, "__init__.py")
long_description = open('README.md', 'r').read()

verstr = "unknown"
try:
    verstrline = open(VERSIONFILE, "rt").read()
except EnvironmentError:
    pass  # Okay, there is no version file.
else:
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        __version__ = mo.group(1)
    else:
        msg = "if %s.py exists, it is required to be well-formed" % VERSIONFILE
        raise RuntimeError(msg)

setup(
    name=PKG,
    version=__version__,
    packages=['mpris_scrobbler'],
    package_dir={'mpris_scrobbler': 'mpris_scrobbler'},
    package_data={
        'mpris_scrobbler': ['*.py', 'services/*.py'],
    },
    scripts=['scripts/mpris_scrobbler'],
    author='Sina Mashek',
    author_email='sina@mashek.xyz',
    maintainer='Sina Mashek',
    maintainer_email='sina@mashek.xyz',
    long_description=long_description,
    description="Scrobbler that can use any MPRIS-enabled media players.",
    license='MIT',
    url='https://git.mashek.net/bottitytto/mpris_scrobbler',
    platforms=['any'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)
