# Author: Jonathan Slenders, City Live

from django.template import Node, NodeList
from django.template import TemplateSyntaxError, VariableDoesNotExist
from django.template import Library
from django.conf import settings


"""
    {% ifdebug %} ... {% endifdebug %}

    Only renders the content of this node when django.conf.settings.DEBUG has
    been set.


    TODO: support {% else %}, (it's easy here, but more complex to make the
          preprocessor support it as well...)
"""

register = Library()

class IfDebugNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def __iter__(self):
        for node in self.nodelist:
            yield node

    def get_nodes_by_type(self, nodetype):
        nodes = []
        if isinstance(self, nodetype):
            nodes.append(self)
        nodes.extend(self.nodelist.get_nodes_by_type(nodetype))
        return nodes

    def render(self, context):
        if settings.DEBUG:
            return self.nodelist.render(context)
        else:
            return u''

@register.tag(name='ifdebug')
def ifdebug(parser, token):
    nodelist = parser.parse(('endifdebug', ))
    parser.delete_first_token()

    return IfDebugNode(nodelist)
