import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="aurorapy",
    version="0.1.1",
    description='Python implementation of Aurora Protocol',
    author="E.Va Energie Valsabbia",
    author_email="it@energievalsabbia.it",
    maintainer='Claudio Catterina',
    maintainer_email='ccatterina@energievalsabbia.it',
    license='MIT',
    packages=['aurorapy'],
    url='https://code.energievalsabbia.it/ccatterina/aurorapy',
    install_requires=[
        'pyserial>=3.2.1',
        'PyCRC>=1.21',
    ],
    classifiers=(
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    )
)
