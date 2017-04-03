from __future__ import print_function

import sys
import warnings
from setuptools import setup, find_packages, Extension
from setuptools.command.install import install


py2 = sys.version < '3'
py3 = sys.version >= '3'

class netbase_python_install(install):
    def run(self):
        print("please type `install`.\n")
        mode = None
        return install.run(self)

cmdclass = {}
ext_modules = []
cmdclass.update({'install': netbase_python_install})

def smart_packages():
    if py2: 
        xs= find_packages(exclude=["py3","netbase/py3","netbase.py3"]) #  packages only , not files
        print(xs)
        return xs
    if py3: return find_packages()

setup(
    cmdclass=cmdclass,
    ext_modules=ext_modules,
    name='Netbase',
    version="0.1.19",
    author="Pannous",
    author_email="info@pannous.com",
    # https://github.com/pannous/netbase
    packages=smart_packages(),
    description='Netbase : Wikidata World Graph',
    license='Apache2 license',
    long_description=open('README.md', 'rb').read().decode('utf8'),
    dependency_links=['git+http://github.com/pannous/netbase-python.git#egg=netbase-python'],
    install_requires=['dill'],
    scripts=[],
    package_data={
        # '': ['*.xml'],
    },
)
