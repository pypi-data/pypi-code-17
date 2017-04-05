import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='hexomega',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',  # example license
    description='A package to streamline creation of projects and tasks for Murdoch University.',
    long_description=README,
    url='https://www.github.com/defstryker/Hex-Omega',
    author='Abhi Rudra',
    author_email='defstryker@hotmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10', 
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
    	'schedule',
		'django',
		'mysqlclient',
		'whitenoise',
		'django-guardian',
		'django-annoying',
		'parse',
		'yattag',
		'haikunator',
		'django-bootstrap3',
		'django-bootstrap-datepicker',
		'django-filter',
		'dj_database_url',
		'psycopg2',
    ],
)