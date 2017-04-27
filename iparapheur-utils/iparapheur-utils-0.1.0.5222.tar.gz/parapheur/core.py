#!/usr/bin/env python
# coding=utf-8

# Récupération de l'objet 'parapheur' et de la configuration
import requests
# Parapheur API
import parapheur
# Scripts API
import scripts
# arguments
import gettext
from requests.packages.urllib3.exceptions import SubjectAltNameWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SubjectAltNameWarning)

__author__ = 'Lukas Hameury'

__all__ = ['init', 'echo', 'check']


def convertmessages(s):
    subdict = \
        {'positional arguments': 'Arguments',
         'optional arguments': 'Arguments',
         'show this help message and exit': 'Affiche ce message et quitte'}
    if s in subdict:
        s = subdict[s]
    return s
gettext.gettext = convertmessages
import argparse


def init():
    parser = argparse.ArgumentParser(
        prog='ph-init',
        description="Génère un fichier de configuration par défaut dans le répertoire courant")
    parser.add_argument('-p', help='Chemin du fichier de configuration')
    parser.add_argument('-c', help='Commande pour laquelle générer le fichier de configuration',
                        choices=["recuparchives"])

    args = parser.parse_args()

    filename = "script"
    path = "."
    if args.p:
        path = args.p
    if args.c:
        filename = args.c

    # Copy the configuration file
    parapheur.copyconfig(filename, path)

    print("Fichier de configuration 'iparapheur-utils.cfg' créé")


def echo():
    parser = argparse.ArgumentParser(
        prog='ph-echo',
        description="Lance un echo via webservice sur un iParapheur")

    parser.add_argument('-s', help="URL du serveur iParapheur")
    parser.add_argument('-c', help='Fichier de configuration')
    parser.add_argument('-u', help='Utilisateur')
    parser.add_argument('-p', help='Mot de passe')

    args = parser.parse_args()

    if args.c:
        parapheur.setconfig(args.c)
    if args.s:
        parapheur.setconfigproperty("server", args.s)
    if args.u:
        parapheur.setconfigproperty("username", args.u)
    if args.p:
        parapheur.setconfigproperty("password", args.p)

    # Initialisation d'API SOAP
    webservice = parapheur.getsoapclient()
    print(webservice.call().echo("coucou"))


def check():
    scripts.checkinstallation()


def recuparchives():
    parser = argparse.ArgumentParser(
        prog='ph-recupArchives',
        description="Lance une récupération / purge des archives")

    parser.add_argument('-s', help="URL du serveur iParapheur")
    parser.add_argument('-c', help='Fichier de configuration')
    parser.add_argument('-u', help='Utilisateur')
    parser.add_argument('-p', help='Mot de passe')

    parser.add_argument('-f', help='Répertoire de destination')
    parser.add_argument('-ps', help='Taille des pages à récupérer')
    parser.add_argument('-r', help='Chemins réduis des téléchargements', choices=["true", "false"])
    parser.add_argument('-pu', help='Active la purge les données', choices=["true", "false"])
    parser.add_argument('-d', help='Télécharge les données', choices=["true", "false"])
    parser.add_argument('-t', help='Filtre sur type')
    parser.add_argument('-st', help='Filtre sur sous-type')
    parser.add_argument('-w', help='Délai de conservation des données')

    args = parser.parse_args()

    if args.c:
        parapheur.setconfig(args.c)
    if args.s:
        parapheur.setconfigproperty("server", args.s)
    if args.u:
        parapheur.setconfigproperty("username", args.u)
    if args.p:
        parapheur.setconfigproperty("password", args.p)

    if args.f:
        parapheur.setconfigproperty("folder", args.f)
    if args.ps:
        parapheur.setconfigproperty("page_size", args.ps)
    if args.r:
        parapheur.setconfigproperty("use_reduced_download_path", args.r)
    if args.pu:
        parapheur.setconfigproperty("purge", args.pu)
    if args.d:
        parapheur.setconfigproperty("download", args.d)
    if args.t:
        parapheur.setconfigproperty("type_filter", args.t)
    if args.st:
        parapheur.setconfigproperty("subtype_filter", args.st)
    if args.w:
        parapheur.setconfigproperty("waiting_days", args.w)

    # Lancement du script
    scripts.recuparchives()


def properties_merger():
    scripts.properties_merger()


if __name__ == "__main__":
    properties_merger()
