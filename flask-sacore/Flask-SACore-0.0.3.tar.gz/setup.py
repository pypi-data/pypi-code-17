"""
Flask-SACore
----------------
SQLAlchemy Core extension for Flask
"""
from setuptools import setup


setup(
    name='Flask-SACore',
    version='0.0.3',
    url='https://github.com/jjmurre/flask-sacore',
    license='MIT',
    author='Jan Murre',
    author_email='jan.murre@catalyz.nl',
    description='SQLAlchemy Core extension for Flask',
    long_description=__doc__,
    packages=['flask_sacore'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.10.1',
        'SQLAlchemy'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
