from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = 0.12

install_requires = [
"netCDF4",
"dwell",
"palettable",
"matplotlib",
"seaborn",
"tables",
"pandas",
"progressbar",
"six"
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
]

setup(name='pydwrf',
    version=version,
    description="DART/WRF utilities in python",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='',
    author='Christopher Lee',
    author_email='lee@aeolisresearch.com',
    url='',
    license='BSD',
    packages=find_packages('src'), #['pydwrf','pydwrf.tes','pydwrf.wrf'],
    package_dir = {'':'src'},#{ 'pydwrf': 'src/pydwrf',
                  #  'pydwrf.tes': "src/pydwrf/tes",
                  #  'pydwrf.wrf': "src/pydwrf/wrf"
                  #  },
    
    package_data={'pydwrf.tes': ['data/*.txt']},
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            [ 'pytes=pydwrf.tes:main',
              # 'wrfobserve=pydwrf.wrf.observe:main',
              #'wrfobservem24=pydwrf.wrf.observem24:main',
              'icemass=pydwrf.wrf.icemass:main',
              'viking_lander=pydwrf.wrf.vl.viking_lander:main',
              'process_nc=pydwrf.wrf.process_nc:main',
              'wrfpostprocess=pydwrf.wrf.postprocess:main',
              'wrfpostprocess_plots=pydwrf.wrf.postprocess_plots:main'

              ]
    }
)
