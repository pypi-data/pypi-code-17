from itertools import cycle as itertools_cycle

from django.template import Node
from django.template import TemplateSyntaxError
from django.template import Library

register = Library()

class CycleNode(Node):
    def __init__(self, cyclevars, variable_name=None):
        self.cyclevars = cyclevars
        self.variable_name = variable_name

    def render(self, context):
        if not hasattr(context, 'cycle_nodes'):
            context.cycle_nodes = {}

        if self.cyclevars is None:
            name = 'CycleNode_%s' % self.variable_name
            if not name in context.cycle_nodes:
                raise TemplateSyntaxError("Named cycle '%s' does not exist" % name)
            node = context.cycle_nodes[name]
        else:
            if self not in context.cycle_nodes:
                context.cycle_nodes[self] = itertools_cycle(self.cyclevars)
                if self.variable_name:
                    # saving self also under a discoverable name
                    name = 'CycleNode_%s' % self.variable_name
                    context.cycle_nodes[name] = self
            node = self

        cycle_iter = context.cycle_nodes[node]
        value = cycle_iter.next().resolve(context)

        if self.variable_name and self.cyclevars is not None:
            context[self.variable_name] = value
            return ''
        else:
            return value

@register.tag
def cycle(parser, token):
    """
    Cycles among the given strings each time this tag is encountered.

    Within a loop, cycles among the given strings each time through
    the loop::

        {% for o in some_list %}
            <tr class="{% cycle 'row1' 'row2' %}">
                ...
            </tr>
        {% endfor %}

    Outside of a loop, give the values a unique name the first time you call
    it, then use that name each sucessive time through::

            <tr class="{% cycle 'row1' 'row2' 'row3' as rowcolors %}">...</tr>
            <tr class="{% cycle rowcolors %}">...</tr>
            <tr class="{% cycle rowcolors %}">...</tr>

    You can use any number of values, separated by spaces. Commas can also
    be used to separate values; if a comma is used, the cycle values are
    interpreted as literal strings.
    """

    # Note: This returns the exact same node on each {% cycle name %} call;
    # that is, the node object returned from {% cycle a b c as name %} and the
    # one returned from {% cycle name %} are the exact same object. This
    # shouldn't cause problems (heh), but if it does, now you know.
    #
    # Ugly hack warning: This stuffs the named template dict into parser so
    # that names are only unique within each template (as opposed to using
    # a global variable, which would make cycle names have to be unique across
    # *all* templates.

    args = token.split_contents()

    if len(args) < 2:
        raise TemplateSyntaxError("'cycle' tag requires at least two arguments")

    if ',' in args[1]:
        # Backwards compatibility: {% cycle a,b %} or {% cycle a,b as foo %}
        # case.
        args[1:2] = ['"%s"' % arg for arg in args[1].split(",")]

    if len(args) == 2:
        # {% cycle foo %} case.
        name = args[1]
        return CycleNode(None, name)
    elif len(args) > 4 and args[-2] == 'as':
        name = args[-1]
        values = [parser.compile_filter(arg) for arg in args[1:-2]]
        node = CycleNode(values, name)
        if not hasattr(parser, '_namedCycleNodes'):
            parser._namedCycleNodes = {}
        parser._namedCycleNodes[name] = node
    else:
        values = [parser.compile_filter(arg) for arg in args[1:]]
        node = CycleNode(values)
    return node
