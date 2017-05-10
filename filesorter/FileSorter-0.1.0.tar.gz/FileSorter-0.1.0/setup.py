from setuptools import setup, find_packages
setup(
    name="FileSorter",
    version="0.1.0",
    packages=find_packages(),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['docutils>=0.3', 'fire>=0.1.0', 'simplejson>=3.10.0'],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.json']
    },
    entry_points={
        'console_scripts': [
            'file_sort = file_sort:main'
        ]
    },

    # metadata for upload to PyPI
    author="Daniel Alexander Ross Evans",
    author_email="me@danielarevans.com",
    description="This is an package to organize files by common data type",
    license="MIT",
    keywords="files organizer organize file management",
    url="http://github.com/migetman9/file_sort"
)
