
from setuptools import setup

setup(
    name='eventpipe-python-client',
    version='0.1.0',
    url='https://github.com/bcambel/event-pipe-client-py/',
    license='Unlicense',
    author='Bahadir Cambel',
    author_email='bcambel@gmail.com',
    description='A Python client to the Event Pipe',
    long_description=__doc__,
    packages=['eventpipe'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'requests>=2.13.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
