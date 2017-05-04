# Author: Jonathan Slenders

from django import template
from django.conf import settings
from django.template import Library, Node, Template, resolve_variable
from django.template import NodeList, Variable, Context
from django.template import TemplateSyntaxError, VariableDoesNotExist
from cgi import escape


"""

    Usage:
    {% inline_edit class_instance 'field_name' %}
    e.g.
    {% inline_edit profile 'address' %}


    Will output:
    <span db:id="323" db:class="profile">...</span>
"""


register = template.Library()


class InlineEditNode(Node):
    def __init__(self, instance, fieldname):
        self.instance = instance
        self.fieldname = fieldname

    def render(self, context):
        try:
            instance = resolve_variable(self.instance, context)
            fieldname = resolve_variable(self.fieldname, context)

            if instance:
                return u'<span class="inline-edit" db:id="%s" db:class="%s" db:field="%s">%s</span>' % (
                        instance.id,
                        escape(instance.__class__.__name__),
                        escape(fieldname),
                        escape(getattr(instance, fieldname)))
            else:
               # Catch None
               return u''

        except VariableDoesNotExist:
            return 'VariableDoesNotExist while rendering {% inline_edit %}'

@register.tag
def inline_edit(parser, token):
    args = token.split_contents()

    if len(args) == 3:
        return InlineEditNode(args[1], args[2])
    else:
        raise template.TemplateSyntaxError


