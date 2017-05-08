from distutils.core import setup
from setuptools import find_packages

INSTALL_REQUIREMENTS = [
    'pcart-core>=1.99',
    'pcart-catalog>=1.99',
    'pcart-customers>=1.99',
    'pcart-cart>=1.99',
    'pcart-messaging>=1.99',
    'lxml>=3.7.3',
    'pytz>=2016.10',
    'pytils>=0.3',
]

setup(
    name='pcart-1c-soap-api',
    version='1.99',
    author='Oleh Korkh',
    author_email='oleh.korkh@the7bits.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    license='BSD License',
    description='A powerful e-commerce solution for Django CMS',
    long_description=open('README.txt').read(),
    platforms=['OS Independent'],
    url='http://the7bits.com/',
    install_requires=INSTALL_REQUIREMENTS,
)