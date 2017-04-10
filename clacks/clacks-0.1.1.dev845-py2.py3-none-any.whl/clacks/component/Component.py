#!/usr/bin/env python3

""" base (effectively abstract) class for CMS Components """


class Component():
    """ base (effectively abstract) class for CMS Components """

    def __init__(self):
        """nothing fancy to do"""
        self.node = None
        self._placement = None

    def startup(self, node):
        """ called by CPage before placing it on page """
        self.node = node

    @property
    def placement(self):
        """ default, mosst used placement returned """
        return self._placement
