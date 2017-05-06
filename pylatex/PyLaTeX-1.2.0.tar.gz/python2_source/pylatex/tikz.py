# -*- coding: utf-8 -*-
u"""
This module implements the classes used to show plots.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""


from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from builtins import super
from future import standard_library
standard_library.install_aliases()
from .base_classes import LatexObject, Environment, Command
from .package import Package
from itertools import izip


class TikZ(Environment):
    u"""Basic TikZ container class."""

    _latex_name = u'tikzpicture'
    packages = [Package(u'tikz')]


class Axis(Environment):
    u"""PGFPlots axis container class, this contains plots."""

    packages = [Package(u'pgfplots'), Command(u'pgfplotsset', u'compat=newest')]

    def __init__(self, options=None, **_3to2kwargs):
        if 'data' in _3to2kwargs: data = _3to2kwargs['data']; del _3to2kwargs['data']
        else: data = None
        u"""
        Args
        ----
        options: str, list or `~.Options`
            Options to format the axis environment.
        """

        super(Axis, self).__init__(options=options, data=data)


class Plot(LatexObject):
    u"""A class representing a PGFPlot."""

    packages = [Package(u'pgfplots'), Command(u'pgfplotsset', u'compat=newest')]

    def __init__(self, name=None, func=None, coordinates=None,
                 error_bar=None, options=None):
        u"""
        Args
        ----
        name: str
            Name of the plot.
        func: str
            A function that should be plotted.
        coordinates: list
            A list of exact coordinates tat should be plotted.

        options: str, list or `~.Options`
        """

        self.name = name
        self.func = func
        self.coordinates = coordinates
        self.error_bar = error_bar
        self.options = options

        super(Plot, self).__init__()

    def dumps(self):
        u"""Represent the plot as a string in LaTeX syntax.

        Returns
        -------
        str
        """

        string = Command(u'addplot', options=self.options).dumps()

        if self.coordinates is not None:
            string += u' coordinates {%\n'

            if self.error_bar is None:
                for x, y in self.coordinates:
                    # ie: "(x,y)"
                    string += u'(' + unicode(x) + u',' + unicode(y) + u')%\n'

            else:
                for (x, y), (e_x, e_y) in izip(self.coordinates,
                                              self.error_bar):
                    # ie: "(x,y) +- (e_x,e_y)"
                    string += u'(' + unicode(x) + u',' + unicode(y) + \
                        u') +- (' + unicode(e_x) + u',' + unicode(e_y) + u')%\n'

            string += u'};%\n%\n'

        elif self.func is not None:
            string += u'{' + self.func + u'};%\n%\n'

        if self.name is not None:
            string += Command(u'addlegendentry', self.name).dumps()

        super(Plot, self).dumps()

        return string
