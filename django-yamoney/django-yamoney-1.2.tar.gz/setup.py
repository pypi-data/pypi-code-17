import os
from setuptools import setup, find_packages
import yamoney

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-yamoney',
    version=yamoney.__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A simple Django app for Yandex.Money service',
    long_description=README,
    author='Mpower',
    author_email='mpower.public@yandex.ru',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=1.8',
        'django-appconf>=1.0.2',
        'python-dateutil>=2.4'
    ],
    test_suite='runtests.runtests'
)
