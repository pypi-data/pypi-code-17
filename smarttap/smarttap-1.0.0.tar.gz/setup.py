try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='smarttap',
    version='1.0.0',
    description='Public transport smart card data analysis software',
    packages=['smarttap'],
    install_requires=['sqlalchemy>=1.1.4'],
    url='https://github.com/JohnTasker/SmartTAP',
    license='GNU GPL V3',
    author='John Tasker',
    author_email='john.tasler@uq.edu.au',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ]
)
