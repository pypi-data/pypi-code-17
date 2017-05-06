#-*- encoding: UTF-8 -*-

from setuptools import setup, find_packages

"""
打包的用的setup必须引入，
"""

VERSION = '0.1.1'

setup(
    name='tci',
    version=VERSION,
    description="a dict for linux cli",
    long_description='just enjoy',
    keywords='python dict terminal',
    author='mapan',
    author_email='mapan1024@gmail.com',
    url='https://github.com/mapan1984/tci',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
    
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
    
        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',
    
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
    ],
    entry_points={
        'console_scripts':[
            'tci = tci.dict:main'
        ]
    },
)
