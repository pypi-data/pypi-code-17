import os
from setuptools import setup

VERSION = "0.0.4.2"

readme = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README")

setup(
    name="dandan",
    version=VERSION,
    description="Several tools for internet",
    long_description=open(readme).read(),
    packages=["dandan"],
    install_requires=[
        "requests",
        "BeautifulSoup4",
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    author="ccyg",
    author_email="kjp1314@163.com",
    url="https://github.com/ccyg/dandan",
    license="MIT",
    include_package_data=True,
    zip_safe=True,
    platforms="any",
)
