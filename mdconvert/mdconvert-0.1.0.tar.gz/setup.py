import setuptools
from os.path import join

# should be loaded below
__version__ = None
name = "mdconvert"

with open(join(name, '_version.py')) as version:
    exec(version.read())

setuptools.setup(
    name=name,
    version=__version__,
    description="configure nbconvert from ipynb",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points=dict(
        console_scripts=['jupyter-mdconvert = mdconvert:launch_instance']),
    tests_require=["pytest"],
    license="BSD-3-Clause")
