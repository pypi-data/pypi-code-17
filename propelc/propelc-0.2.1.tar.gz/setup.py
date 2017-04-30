import re
import ast
from setuptools import setup

_version_file = "propelc.py"
with open(_version_file, 'rb') as f:
    _version_re = re.compile(r'__version__\s+=\s+(.*)')
    __version__ = str(ast.literal_eval(_version_re.search(f.read().decode('utf-8')).group(1)))


setup(
    name="propelc",
    version=__version__,
    author="Mardix",
    py_modules=['propelc'],
    entry_points=dict(console_scripts=[
        'propelc=propelc:cmd',
    ]),
    include_package_data=True,
    install_requires=[
        "ansible>=2.2",
        "sh==1.11",
        "boto==2.39.0",
        "tld==0.7.2",
        "pyyaml>=3.11"
    ],
    zip_safe=False
)

