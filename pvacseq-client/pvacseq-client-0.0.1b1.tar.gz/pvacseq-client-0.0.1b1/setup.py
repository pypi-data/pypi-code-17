from setuptools import setup
import os
import json

data_files = []
for dirpath, dirnames, filenames in os.walk(__file__):
    for filename in filenames:
        if not (filename.endswith(".py") or filename.endswith(".pyc")):
            data_files.append(os.path.join('..', dirpath, filename))


setup(
    name="pvacseq-client",
    version=json.load(open("package.json"))['version']+"b1",
    packages=["src"],
    package_data={
        'src' : data_files,
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',

        "Programming Language :: Python :: 3.5"
    ],
    zip_safe=False,

    author = "Josh McMichael, Jasreet Hundal, Susanna Kiwala, Aaron Graubert, Jason Walker, Chris Miller, Malachi Griffith and Elaine Mardis",
    author_email = "pvacseq-support@genome.wustl.edu",
    description = "Web Front-End for pVAC-Seq",
    long_description = "A web client to manage and visualize data for pVAC-Seq",
    license = "NPOSL-3.0",
    keywords = "antigens neoantigens cancer sequencing variant variants",
    url = "https://github.com/griffithlab/pVAC-Seq-Client",   #
)
