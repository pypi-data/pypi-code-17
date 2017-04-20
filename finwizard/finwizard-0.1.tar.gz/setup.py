from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="finwizard",
    version="0.1",
    packages=['finwizard'],
    install_requires=[
        'pandas',
        'numpy'],
    zip_safe= False,
    # metadata for upload to PyPI
    author="JEBBS",
    author_email="jasonsporter88@gmail.com",
    description="This package is a personal finance tool.",
    license="JSP",
    keywords="finwizard personal finance plan budget",
    url="http://gitlab.com/porterjs/finwizard",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)
