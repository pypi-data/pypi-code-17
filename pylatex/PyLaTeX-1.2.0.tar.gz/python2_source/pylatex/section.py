# -*- coding: utf-8 -*-
u"""
This module implements the section type classes.

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
from .base_classes import Container, Command


class Section(Container):
    u"""A class that represents a section."""

    #: A section should normally start in its own paragraph
    end_paragraph = True

    #: Number the sections, by changing the `~.Section` class default all
    #: subclasses will also have the new default.
    numbering = True

    def __init__(self, title, numbering=None, **kwargs):
        u"""
        Args
        ----
        title: str
            The section title.
        numbering: bool
            Add a number before the section title.
        """

        self.title = title

        if numbering is not None:
            self.numbering = numbering

        super(Section, self).__init__(**kwargs)

    def dumps(self):
        u"""Represent the section as a string in LaTeX syntax.

        Returns
        -------
        str

        """

        if not self.numbering:
            num = u'*'
        else:
            num = u''

        string = Command(self.latex_name + num, self.title).dumps()
        string += u'%\n' + self.dumps_content()

        return string


class Subsection(Section):
    u"""A class that represents a subsection."""


class Subsubsection(Section):
    u"""A class that represents a subsubsection."""
