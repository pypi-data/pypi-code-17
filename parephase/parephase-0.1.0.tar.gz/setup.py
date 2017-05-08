#!/usr/bin/env python
from setuptools import setup
import versioneer

setup(
    name="parephase",
    install_requires=[
        "gffutils",
        "numpy",
        "pysam",
        "docopt",
    ],
    packages=["parephase"],
    version=versioneer.get_version(),
    entry_points={
        'console_scripts': [
            'parephase = parephase:main',
        ],
    },
    cmdclass=versioneer.get_cmdclass(),
    author="Kevin D. Murray",
    author_email="kdmpapers@gmail.com",
    description="Detects phasing of 5'PARE data around stop codons",
    license="MPL2",
    url="https://github.com/kdmurray91/parephase",
    keywords="bioinformatics PARE RNA",
)
