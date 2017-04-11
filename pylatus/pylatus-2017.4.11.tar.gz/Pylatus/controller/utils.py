#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import math
from scipy import constants


SI = 3.1356


def pyqt2bool(entry):
    return not (entry == 'false' or not entry)


def createPath(path, home):
    """Creates the full path in the home directory"""
    if path.startswith('/'):
        path = path[1:]

    fullPath = home
    for dirr in path.split('/'):
        fullPath = os.path.join(fullPath, dirr)
        if not os.path.exists(fullPath):
            os.mkdir(fullPath)
        elif os.path.isfile(fullPath):
            os.remove(fullPath)
            os.mkdir(fullPath)
    return fullPath


def wavelength(mono):
    """mono angle --> wave length"""
    return 2 * SI * math.sin(math.radians(mono))


def energy(mono):
    """mono angle --> energy"""
    return constants.c * constants.h / constants.eV * 1e7 / wavelength(mono)


def angle(wl):
    """wave length --> mono angle"""
    return math.degrees(math.asin(wl / SI / 2))


def calcTime(uptime):
    if uptime < 60:
        days, hours, minutes = 0, 0, int(math.floor(uptime))
    elif 60 <= uptime < 60 * 24:
        hours = int(uptime // 60)
        minutes = int(math.floor(uptime - hours * 60))
        days = 0
    else:
        days = int(uptime // (60 * 24))
        hours = int(uptime // 60 - days * 24)
        minutes = int(math.floor(uptime - days * 60 * 24 - hours * 60))
    return days, hours, minutes
