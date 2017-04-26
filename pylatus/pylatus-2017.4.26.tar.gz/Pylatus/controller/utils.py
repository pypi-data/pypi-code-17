#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import math


SI = 3.1356
LAMBDA = 12.398419739640717  # c * h / ev * 1e7


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
    return LAMBDA / wavelength(mono)


def angle(wl):
    """wave length --> mono angle"""
    return math.degrees(math.asin(wl / SI / 2))
