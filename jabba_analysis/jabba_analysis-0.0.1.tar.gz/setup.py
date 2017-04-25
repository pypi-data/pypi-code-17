from distutils.core import setup
from setuptools import find_packages

setup(
        name="jabba_analysis",
        packages=find_packages(),
        version="0.0.1",
        description="Additional JABBA analysis functions",
        author="missingdays",
        author_email="rebovykin@gmail.com",
        url="https://github.com/missingdays/jabba_analysis",
        download_url="https://github.com/missingdays/jabba_analysis/arhive/0.0.1.tar.gz",
        keywords=["JABBA", "Jenkins"],
        install_requires=["jabba"]
)

