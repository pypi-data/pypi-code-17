##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Manager Details View

"""
__docformat__ = "reStructuredText"
import zope.component

from zope.publisher.browser import BrowserView
from zope.generations.interfaces import ISchemaManager

import docutils.core


class _ReStructuredTextToHTMLRenderer(BrowserView):
    r"""An Adapter to convert from Restructured Text to HTML.

    Examples::

      >>> from zope.publisher.browser import TestRequest
      >>> source = u'''
      ... This is source.
      ...
      ... Header 3
      ... --------
      ... This is more source.
      ... '''
      >>> renderer = _ReStructuredTextToHTMLRenderer(source, TestRequest())
      >>> print(renderer.render().strip())
      <p>This is source.</p>
      <div class="section" id="header-3">
      <h3>Header 3</h3>
      <p>This is more source.</p>
      </div>
    """

    # Lifted from zope.app.renderers.rest

    def render(self, settings_overrides={}):
        """See zope.app.interfaces.renderer.IHTMLRenderer

        Let's make sure that inputted unicode stays as unicode:

        >>> renderer = _ReStructuredTextToHTMLRenderer(u'b\xc3h', None)
        >>> output = renderer.render()
        >>> isinstance(output, bytes)
        False


        >>> text = u'''
        ... =========
        ... Heading 1
        ... =========
        ...
        ... hello world
        ...
        ... Heading 2
        ... ========='''
        >>> overrides = {'initial_header_level': 2,
        ...              'doctitle_xform': 0 }
        >>> renderer = _ReStructuredTextToHTMLRenderer(text, None)
        >>> print(renderer.render(overrides))
        <div class="section" id="heading-1">
        <h2>Heading 1</h2>
        <p>hello world</p>
        <div class="section" id="heading-2">
        <h3>Heading 2</h3>
        </div>
        </div>
        <BLANKLINE>
        """
        # default settings for the renderer
        overrides = {
            'halt_level': 6,
            'input_encoding': 'unicode',
            'output_encoding': 'unicode',
            'initial_header_level': 3,
            }
        overrides.update(settings_overrides)
        parts = docutils.core.publish_parts(
            self.context,
            writer_name='html',
            settings_overrides=overrides,
            )
        return u''.join((parts['body_pre_docinfo'], parts['docinfo'], parts['body']))

class ManagerDetails(object):
    r"""Show Details of a particular Schema Manager's Evolvers

    This method needs to use the component architecture, so
    we'll set it up:

      >>> from zope.component.testing import setUp, tearDown
      >>> setUp()

    We need to define some schema managers.  We'll define just one:

      >>> from zope.generations.generations import SchemaManager
      >>> from zope import component as ztapi
      >>> app1 = SchemaManager(0, 3, 'zope.generations.demo')
      >>> ztapi.provideUtility(app1, ISchemaManager, 'foo.app1')

    Now let's create the view:

      >>> from zope.publisher.browser import TestRequest
      >>> details = ManagerDetails()
      >>> details.context = None
      >>> details.request = TestRequest(environ={'id': 'foo.app1'})

    Let's now see that the view gets the ID correctly from the request:

      >>> details.id
      'foo.app1'

    Now check that we get all the info from the evolvers:

      >>> info = details.getEvolvers()
      >>> for item in info:
      ...     print(sorted(item.items()))
      [('from', 0), ('info', u'<p>Evolver 1</p>\n'), ('to', 1)]
      [('from', 1), ('info', u'<p>Evolver 2</p>\n'), ('to', 2)]
      [('from', 2), ('info', ''), ('to', 3)]

    We'd better clean up:

      >>> tearDown()
    """

    request = None
    context = None

    id = property(lambda self: self.request['id'])

    def getEvolvers(self):
        id = self.id
        manager = zope.component.getUtility(ISchemaManager, id)

        evolvers = []

        for gen in range(manager.minimum_generation, manager.generation):

            info = manager.getInfo(gen + 1)
            if info is None:
                info = ''
            else:
                renderer = _ReStructuredTextToHTMLRenderer(
                    info.decode('utf-8') if isinstance(info, bytes) else info,
                    self.request)
                info = renderer.render()

            evolvers.append({'from': gen, 'to': gen + 1, 'info': info})

        return evolvers
