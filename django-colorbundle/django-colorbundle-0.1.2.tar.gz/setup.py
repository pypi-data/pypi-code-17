from setuptools import setup, find_packages

from colorbundle import __version__

setup(
    name='django-colorbundle',
    version=__version__,
    description='Template filters for extracting colours from an image.',
    long_description=open('README.rst').read(),
    author='Jeff Nelson',
    author_email='rustyangel+pypi@gmail.com',
    url='https://github.com/stormwarning/django-colorbundle',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'colorgram.py>=1.1.0'
    ],
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Utilities',
    )
)
