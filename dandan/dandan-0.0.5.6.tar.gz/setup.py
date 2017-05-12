import os
import sys
from setuptools import setup

base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
try:
    import dandan
    version = dandan.__version__
except Exception:
    print "import project error"
    exit(0)

readme = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README")

setup(
    name="dandan",
    version=dandan.__version__,
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
