from setuptools import setup

setup(
    name='graf-py',
    version='0.1.1',
    description='Graf Python Client',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: System :: Logging',
        'Topic :: System :: Monitoring',
        'Topic :: Software Development :: Quality Assurance'
    ],
    keywords='graf iograf metrics events',
    url='http://github.com/iograf/graf-py',
    author='Victor Gama',
    author_email='hey@vito.io',
    license='MIT',
    packages=['graf'],
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose', 'mock']
)
