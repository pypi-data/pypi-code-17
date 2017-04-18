#!/usr/bin/env python
VERSION="0.8.1"
AUTHOR="Joon Ro"
EMAIL="joon.ro@outlook.com"
DESC="Color Schemes for Jupyter Qt Console"
NAME="jupyter_qtconsole_colorschemes"
URL="https://bitbucket.org/joon/color-schemes-for-jupyter-qt-console"
from setuptools import setup

DOWNLOAD_URL = URL + "/get/v{}.zip".format(VERSION)

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    download_url=DOWNLOAD_URL,
    description=DESC,
    packages=[NAME],
    package_data={NAME: ["*.css"]},
    entry_points={"pygments.styles": [
        "{style} = {pkgname}.{style}:Base16OceanDarkStyle".format(pkgname=NAME, style='base16_ocean_dark'),
        '{style} = {pkgname}.{style}:MaterialLightStyle'.format(pkgname=NAME, style='material_light'),
        "{style} = {pkgname}.{style}:SolarizeddarkStyle".format(pkgname=NAME, style='solarizeddark'),
        "{style} = {pkgname}.{style}:SolarizedlightStyle".format(pkgname=NAME, style='solarizedlight'),
        "{style} = {pkgname}.{style}:TomorrowStyle".format(pkgname=NAME, style='tomorrow'),
        "{style} = {pkgname}.{style}:ZenburnStyle".format(pkgname=NAME, style='zenburn'),
        "{style} = {pkgname}.{style}:BlackboardStyle".format(pkgname=NAME, style='blackboard'),
    ]})
