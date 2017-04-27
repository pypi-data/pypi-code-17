from setuptools import setup

setup(
    name='cute_format',
    version='0.1.2',

    description='pack data and retrieval in easy way',
    long_description=open('README.rst').read(),

    author='Ming Hsuan Tu',
    author_email='qrnnis2623891@gmail.com',
    url='https://github.com/twmht/cute_format',
    license='MIT License',

    packages=['cute', 'cute.tests'],

    setup_requires=['pytest-runner'],
    tests_require=['pytest'],


    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
)
