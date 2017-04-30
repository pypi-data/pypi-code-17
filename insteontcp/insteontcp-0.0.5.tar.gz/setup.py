import os
import re
from setuptools import setup

REQUIRES = [
    'pyyaml>=3.11,<4'
]

PACKAGE_NAME = 'insteontcp'

setup(
    name = PACKAGE_NAME,
    version = "0.0.5",
    author = "Heath Paddock",
    author_email = "hp@heathpaddock.com",
    description = ("A python package that interacts with the Insteon PLMs directly over their TCP interface"),
    license = "MIT",
    keywords = ["insteon", "hub", "tcp", "plm", "2012", "2242-222"],
    url = "https://github.com/heathbar/insteontcp",
    packages=['insteontcp'],
    include_package_data=True,
    install_requires=REQUIRES,
    classifiers=[
        'Intended Audience :: Developers',
        "Development Status :: 3 - Alpha",
        "Topic :: Home Automation",
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        "License :: OSI Approved :: MIT License",
    ],
)