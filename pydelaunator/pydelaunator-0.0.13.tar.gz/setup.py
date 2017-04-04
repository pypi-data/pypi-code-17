import os
from setuptools   import setup, find_packages
from pip.req      import parse_requirements
from pip.download import PipSession


# access to the file at the package top level (like README)
def path_to(filename):
    return os.path.join(os.path.dirname(__file__), filename)

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements(path_to('requirements.txt'),
                                  session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]


setup(
    name='pydelaunator',
    version='0.0.13',
    packages=find_packages(),
    include_package_data = True,  # read the MANIFEST.in file
    install_requires=reqs,

    author="lucas bourneuf",
    author_email="lucas.bourneuf@openmailbox.org",
    description="quad-edge data structure",
    long_description=open(path_to('README.mkd')).read(),
    keywords="graph data structure",
    url="https://github.com/Aluriak/pydelaunator",

    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
