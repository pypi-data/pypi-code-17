#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import JSTPyGame

setup(
    description='My first Python game',
    long_description=open('README.rst').read(),
    author='Julien SIDOT',
    url='https://github.com/slidest/JSTPyGame',
    author_email='julien.sidot@gmail.com',
    version=JSTPyGame.__version__,
    # Vous pouvez rajouter une liste de dépendances pour votre lib
    # et même préciser une version. A l'installation, Python essayera de
    # les télécharger et les installer.
    #
    # Ex: ["gunicorn", "docutils >= 0.3", "lxml==0.5a7"]
    install_requires=['nose', 'termcolor >= 1.1.0'],
    # Liste les packages à insérer dans la distribution
    # plutôt que de le faire à la main, on utilise la foncton
    # find_packages() de setuptools qui va cherche tous les packages
    # python recursivement dans le dossier courant.
    # C'est pour cette raison que l'on a tout mis dans u
    packages=find_packages(),
    scripts=[],
    name='JSTPyGame',
    # Il est d'usage de mettre quelques metadata à propos de sa lib
    # Pour que les robots puissent facilement la classer.
    # La liste des marqueurs autorisées est longue:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    #
    # Il n'y a pas vraiment de règle pour le contenu. Chacun fait un peu
    # comme il le sent. Il y en a qui ne mettent rien.
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7"
    ],
    license="WTFPL",
    # Active la prise en compte du fichier MANIFEST.in
    include_package_data=True,
    # C'est un système de plugin, mais on s'en sert presque exclusivement
    # Pour créer des commandes, comme "django-admin".
    # Par exemple, si on veut créer la fabuleuse commande "proclame-sm", on
    # va faire pointer ce nom vers la fonction proclamer(). La commande sera
    # créé automatiquement. 
    # La syntaxe est "nom-de-commande-a-creer = package.module:fonction".
    entry_points={
        'console_scripts': [
           'jst-pygame = JSTPyGame.PyGame:start',
        ],
    }
    )
