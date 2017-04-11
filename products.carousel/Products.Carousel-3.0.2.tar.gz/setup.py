# -*- coding: utf-8 -*-
"""
This module contains the tool of Products.Carousel
"""
from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n' +
    open('CONTRIBUTORS.txt').read()
)

tests_require = [
    'Products.PloneTestCase',
    'zope.testing',
]


setup(
    name='Products.Carousel',
    version='3.0.2',
    description="Carousel allows you to add user-configurable rotating "
                "banners to any section of a Plone site.",
    long_description=long_description,
    # Get more strings from
    #  https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.0',
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='plone carousel slideshow banners rotating features',
    author='Groundwire',
    author_email='davidglick@groundwire.org',
    url='https://github.com/collective/Products.Carousel',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products', ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zope.app.component',
        'zope.app.publisher',
        'plone.app.z3cform'],
    tests_require=tests_require,
    extras_require=dict(tests=tests_require),
    test_suite='Products.Carousel.tests.test_docs.test_suite',
    entry_points={
        # -*- Entry points: -*-
        'z3c.autoinclude.plugin': 'target = plone',
    },
)
