import codecs
from setuptools import setup, find_packages

entry_points = {
    "paste.filter_app_factory": [
        "cors = nti.wsgi.cors:cors_filter_factory",
        "cors_options = nti.wsgi.cors:cors_option_filter_factory",
    ],
}


TESTS_REQUIRE = [
    'nti.testing',
    'Paste',
    'WebTest',
    'zope.testrunner',
]


def _read(fname):
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()


setup(
    name='nti.wsgi.cors',
    version=_read('version.txt').strip(),
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="Support for CORS in a WSGI environment",
    long_description=(_read('README.rst') + '\n\n' + _read('CHANGES.rst')),
    url="https://github.com/NextThought/nti.wsgi.cors",
    license='Apache',
    keywords='wsgi cors',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    zip_safe=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    namespace_packages=['nti'],
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'setuptools',
        'greenlet',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
    },
    entry_points=entry_points,
    test_suite="nti.wsgi.cors.tests",
)
