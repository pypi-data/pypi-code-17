from setuptools import setup, find_packages

setup(
    name="mathhero",
    version="0.1",
    packages=['mathhero'],
    install_requires=[
        'pandas',
        'numpy'],
    zip_safe= False,
    # metadata for upload to PyPI
    author="JEBBS",
    author_email="jasonsporter88@gmail.com",
    description="This package integrates mathematical tools for complex data analysis",
    license="JSP",
    keywords="mathhero math hero solver data engineering",
    url="http://gitlab.com/porterjs/mathhero",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)
