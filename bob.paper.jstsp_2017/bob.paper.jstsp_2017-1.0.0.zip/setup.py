#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Fri 3 Feb 13:43:22 2017

# This package iperates under BSD license, see file LICENSE

from setuptools import setup, dist

dist.Distribution(dict(setup_requires=['bob.extension']))

from bob.extension.utils import load_requirements, find_packages

install_requires = load_requirements()

# Define package version
version = open("version.txt").read().rstrip()

# The only thing we do in this file is to call the setup() function with all
# parameters that define our package.
setup(

    name='bob.paper.jstsp_2017',
    version=version,
    description='Impact of score fusion on voice biometrics and presentation attack detection in cross-database evaluations',
    url='http://gitlab.idiap.ch/bob/bob.paper.jstsp_2017',
    license='BSD',
    author='Pavel Korshunov',
    author_email='pavel.korshunov@idiap.ch',
    long_description=open('README.rst').read(),

    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    install_requires=install_requires,

    entry_points={
        'console_scripts': [
            'plot_pad_results.py         =bob.paper.jstsp_2017.plot_pad_results:main',
            'plot_far_frr_pad.py         = bob.paper.jstsp_2017.plot_far_frr_pad:main',
            'plot_det_from_sets.py         = bob.paper.jstsp_2017.plot_det_from_sets:main',
            'fuse_asv_pad_scores.py         = bob.paper.jstsp_2017.fuse_asv_pad_scores:main',
        ],
    },

    classifiers=[
        'Framework :: Bob',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Database :: Front-Ends',
    ],
)
