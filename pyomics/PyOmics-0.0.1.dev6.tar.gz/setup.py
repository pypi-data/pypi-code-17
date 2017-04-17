from setuptools import setup


def setup_package():
    # PyPi doesn't accept markdown as HTML output for long_description
    # Pypandoc is only required for uploading the metadata to PyPi and not installing it by the user

    # Try to covert Mardown to RST file for long_description
    try:
        import pypandoc
        long_description = pypandoc.convert_file('README.md', 'rst')

    # Except ImportError then read in the Markdown file for long_description
    except ImportError:
        print("warning: pypandoc module not found, could not convert Markdown to RST")
        with open('README.md') as f:
            long_description = f.read()

    # Define the meatadata as dictionary
    metadata = dict(
        name='PyOmics',
        version='0.0.1.dev6',
        description='A library for dealing with omic-data in the life sciences',
        long_description=long_description,
        url='https://github.com/FloBay/PyOmics.git',
        author='Florian P. Bayer',
        author_email='f.bayer@tum.de',
        license='MIT',
        classifiers=[
            'Development Status :: 1 - Planning',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Education',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        keywords='PyOmics bioinformatics omics science data analysis easy',
        packages=['PyOmics'],
    )

    # Bundle metadata up
    setup(**metadata)

if __name__ == '__main__':
    setup_package()
