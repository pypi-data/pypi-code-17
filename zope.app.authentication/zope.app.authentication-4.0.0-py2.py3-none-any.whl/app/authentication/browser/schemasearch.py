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
"""Search interface for queriables.

"""
__docformat__ = "reStructuredText"

from zope.app.authentication.i18n import ZopeMessageFactory as _
from zope.formlib.interfaces import IInputWidget, InputErrors
from zope.formlib.interfaces import ISourceQueryView
from zope.formlib.interfaces import WidgetsError, MissingInputError
from zope.formlib.utility import setUpWidgets
from zope.i18n import translate
from zope.interface import implementer
from zope.schema import getFieldsInOrder
from zope.traversing.api import getName, getPath


search_label = _('search-button', 'Search')
source_label = _(u"Source path")
source_title = _(u"Path to the source utility")

@implementer(ISourceQueryView)
class QuerySchemaSearchView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def render(self, name):
        schema = self.context.schema
        sourcename = getName(self.context)
        sourcepath = getPath(self.context)
        setUpWidgets(self, schema, IInputWidget, prefix=name+'.field')
        html = []

        # add sub title for source search field
        html.append('<h4>%s</h4>' % sourcename)

        # start row for path display field
        html.append('<div class="row">')

        # for each source add path of source
        html.append('  <div class="label">')
        label = translate(source_label, context=self.request)
        title = translate(source_title, context=self.request)
        html.append('    <label for="%s" title="%s">' % (sourcename, title))
        html.append('      %s' % label)
        html.append('    </label>')
        html.append('  </div>')
        html.append('  <div class="field">')
        html.append('      %s' % sourcepath)
        html.append('  </div>')
        html.append('</div>')

        # start row for search fields
        html.append('<div class="row">')

        for field_name, _field in getFieldsInOrder(schema):
            widget = getattr(self, field_name+'_widget')

            # for each field add label...
            html.append('  <div class="label">')
            html.append('    <label for="%s" title="%s">'
                        % (widget.name, widget.hint))
            html.append('      %s' % widget.label)
            html.append('    </label>')
            html.append('  </div>')

            # ...and field widget
            html.append('  <div class="field">')
            html.append('    %s' % widget())

            if widget.error(): # pragma: no cover
                html.append('    <div class="error">')
                html.append('      %s' % widget.error())
                html.append('    </div>')
            html.append('  </div>')
        # end row
        html.append('</div>')

        # add search button for search fields
        html.append('<div class="row">')
        html.append('  <div class="field">')
        html.append('    <input type="submit" name="%s" value="%s" />'
                     % (name+'.search',
                        translate(search_label, context=self.request)))
        html.append('  </div>')
        html.append('</div>')

        return '\n'.join(html)

    def results(self, name):
        if (name + '.search') not in self.request:
            return None
        schema = self.context.schema
        setUpWidgets(self, schema, IInputWidget, prefix=name + '.field')
        # XXX inline the original getWidgetsData call in
        # zope.app.form.utility to lift the dependency on zope.app.form.
        data = {}
        errors = []
        for widget_name, field in getFieldsInOrder(schema):
            widget = getattr(self, widget_name + '_widget')
            if IInputWidget.providedBy(widget):
                if widget.hasInput():
                    try:
                        data[widget_name] = widget.getInputValue()
                    except InputErrors as error: # pragma: no cover
                        errors.append(error)
                elif field.required: # pragma: no cover
                    errors.append(MissingInputError(
                        widget_name, widget.label, 'the field is required'))
        if errors: # pragma: no cover
            raise WidgetsError(errors, widgetsData=data)
        return self.context.search(data)
