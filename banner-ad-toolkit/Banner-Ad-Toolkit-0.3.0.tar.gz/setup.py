from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

__version__ = '0.3.0'

setup(
    name='Banner-Ad-Toolkit',
    version=__version__,

    description='A command line tool to aid in the development of banner ad campaigns. Auto generates PSDs at the required sizes with specified filenames to get you started, then when done designing, exports static banners at or under max file sizes specified. All managed via a very simple manifest file.',
    long_description=long_description,

    url='https://bitbucket.org/tsantor/banner-ad-toolkit',
    download_url='https://bitbucket.org/tsantor/banner-ad-toolkit/get/%s.tar.gz' % __version__,
    author='Tim Santor',
    author_email='tsantor@xstudios.agency',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        "Environment :: Console",

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='banner ad',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'python-bash-utils>=0.1.2',
        'progressbar33>=2.4',
        'pillow',
        'cssutils',
    ],

    # If there are data files included in your packages that need to be
    # installed in site-packages, specify them here.  If using Python 2.6 or
    # less, then these have to be included in MANIFEST.in as well.
    include_package_data=True,

    package_data={
        'adkit': [
            'templates/template.html',
        ]
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'adkit-html = adkit.generate_html:main',
            'adkit-upload = adkit.upload_html:main',
            'adkit-css = adkit.generate_css:main',
            'adkit-optimize = adkit.optimize_images:main',
            'adkit-zip = adkit.create_zips:main',
            'adkit-quickstart = adkit.quickstart:main',
        ],
    },
)
