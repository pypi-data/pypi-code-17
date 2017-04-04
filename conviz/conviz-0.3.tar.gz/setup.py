from distutils.core import setup

from setuptools import find_packages

VERSION = "0.3"

setup(
    name="conviz",
    version=VERSION,
    description="A convolutional neural layer visualization library",
    author="Philippe Trempe",
    author_email="ph.trempe@gmail.com",
    license="MIT",
    url="https://github.com/PhTrempe/conviz",
    download_url="https://github.com/phtrempe/conviz/archive/{}.tar.gz".format(
        VERSION),
    keywords=["convolutional", "neural", "network", "layer", "visualization"],
    classifiers=[],
    packages=find_packages(),
    requires=["numpy", "scipy", "pillow", "keras"]
)
