# Author: Jonathan Slenders, City Live

from django.template import Node, NodeList
from django.template import TemplateSyntaxError, VariableDoesNotExist
from django.template import Library, Variable
from django.conf import settings

from cl_utils.translation_utils import language as language_block

"""
    {% language "nl" %} ... {% endlanguage %}

    Renders the content of this node into the given language.
"""

register = Library()

class LanguageNode(Node):
    def __init__(self, nodelist, lang):
        self.nodelist = nodelist
        self.lang = Variable(lang)

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
        with language_block(self.lang.resolve(context)):
            return self.nodelist.render(context)

@register.tag
def language(parser, token):
    nodelist = parser.parse(('endlanguage', ))
    parser.delete_first_token()

    bits = token.contents.split()

    if len(bits) != 2:
        raise TemplateSyntaxError, "{% language 'en' %} requires exactly one parameter "


    return LanguageNode(nodelist, bits[1])
