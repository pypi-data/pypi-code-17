from django.template import TemplateSyntaxError, Variable
from django.template import Library, Node, Template, Context
from django.template.loader import get_template
from django.conf import settings

register = Library()

def render_with_filter(t, filters, context):
    c = context.__dict__.copy()
    c['TEXT___'] = t
    tmpl = '{%% load markup %%}{{ TEXT___|%s }}' % (filters,)
    t = Template(tmpl)
    return t.render(Context(c))

class ConstantIncludeNode(Node):
    def __init__(self, template_path, filters):
        self.filters = filters
        try:
            t = get_template(template_path)
            self.template = t
        except:
            if settings.TEMPLATE_DEBUG:
                raise
            self.template = None

    def render(self, context):
        if self.template:
            t = self.template.render(context)
            return render_with_filter(t, self.filters, context)
        else:
            return ''

class IncludeNode(Node):
    def __init__(self, template_name, filters):
        self.template_name = Variable(template_name)
        self.filters = filters

    def render(self, context):
        try:
            template_name = self.template_name.resolve(context)
            t = get_template(template_name)
            t = t.render(context)
            return render_with_filter(t, self.filters, context)
        except TemplateSyntaxError, e:
            if settings.TEMPLATE_DEBUG:
                raise
            return ''
        except:
            return '' # Fail silently for invalid included templates.

def do_include(parser, token):
    """
    Loads a template and renders it with the current context.

    Example::

        {% include_with_filter "foo/some_include" 'markdown:"toc,def_list,footnotes"' %}
    """
    bits = token.split_contents()
    if len(bits) != 3:
        raise TemplateSyntaxError, "%r tag takes two arguments: the name of the template to be included and a filter list to execute" % bits[0]
    path = bits[1]
    filters = bits[2][1:-1]
    if path[0] in ('"', "'") and path[-1] == path[0]:
        return ConstantIncludeNode(path[1:-1], filters)
    return IncludeNode(bits[1], filters)

register.tag('include_with_filter', do_include)

