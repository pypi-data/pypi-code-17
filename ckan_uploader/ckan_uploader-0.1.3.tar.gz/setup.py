# coding=utf-8
from setuptools import setup

setup(
    name='ckan_uploader',
    version='0.1.3',
    packages={'ckan_uploader': 'ckan_uploader'},
    description='Carga y actualizacion de recursos remotos en una plataforma CKAN 2.5.3+',
    long_description='Librería de python para la carga y actualizacion '
                     'de recursos remotos en una plataforma CKAN 2.5.3+',
    author='Datos Argentina',
    author_email='datos@modernizacion.gob.ar',
    url='https://github.com/datosgobar/ckan-uploader',
    include_package_data=True,
    install_requires=[
        'requests>=2.13.0',
        'ckanapi>=4.0',
        'arrow>=0.10.0',
        'httmock==1.2.6'
    ],
    license="ISCL",
    zip_safe=False,
    keywords='ckan_uploader ckan resources',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ])
