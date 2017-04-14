from setuptools import setup, find_packages


long_description = "QtArgSelector is a simple GUI arguments selector.  " \
                   "https://github.com/drilldripper/QtArgumentSelector"


setup(
    name='QtArgSelector',
    version='1.0.0',
    description='Select program arguments with GUI',
    long_description=long_description,
    url='https://github.com/drilldripper/QtArgSelector',
    author='drilldripper',
    author_email='ryo.kt.in@gmail.com',
    packages=find_packages(),
    license='MIT',
    keywords='PyQt argument',
    platforms=['POSIX', 'Windows', 'Mac OS'],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=[
        'PyQt5'
    ]
)
