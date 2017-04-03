# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from collections import Mapping

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

try:
    from urlparse import urlparse, parse_qs, urlunparse
except ImportError:
    from urllib.parse import urlparse, parse_qs, urlunparse

from django.forms.utils import flatatt
from django.template import Variable, VariableDoesNotExist
from django.template.base import FilterExpression, kwarg_re, TemplateSyntaxError
from django.template.loader import get_template
from django.utils.encoding import force_str, force_text
from django.utils.safestring import mark_safe

try:
    from django.utils.html import format_html
except ImportError:
    from .legacy import format_html_pre_18 as format_html

from .text import text_value

# RegEx for quoted string
QUOTED_STRING = re.compile(r'^["\'](?P<noquotes>.+)["\']$')


def handle_var(value, context):
    """
    Handle template tag variable
    """
    # Resolve FilterExpression and Variable immediately
    if isinstance(value, FilterExpression) or isinstance(value, Variable):
        return value.resolve(context)
    # Return quoted strings unquoted
    # http://djangosnippets.org/snippets/886
    stringval = QUOTED_STRING.search(value)
    if stringval:
        return stringval.group('noquotes')
    # Resolve variable or return string value
    try:
        return Variable(value).resolve(context)
    except VariableDoesNotExist:
        return value


def parse_token_contents(parser, token):
    """
    Parse template tag contents
    """
    bits = token.split_contents()
    tag = bits.pop(0)
    args = []
    kwargs = {}
    asvar = None
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]
    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError(
                    'Malformed arguments to tag "{}"'.format(tag))
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))
    return {
        'tag': tag,
        'args': args,
        'kwargs': kwargs,
        'asvar': asvar,
    }


def split_css_classes(css_classes):
    """
    Turn string into a list of CSS classes
    """
    classes_list = text_value(css_classes).split(' ')
    return [c for c in classes_list if c]


def add_css_class(css_classes, css_class, prepend=False):
    """
    Add a CSS class to a string of CSS classes
    """
    classes_list = split_css_classes(css_classes)
    classes_to_add = [c for c in split_css_classes(css_class)
                      if c not in classes_list]
    if prepend:
        classes_list = classes_to_add + classes_list
    else:
        classes_list += classes_to_add
    return ' '.join(classes_list)


def remove_css_class(css_classes, css_class):
    """
    Remove a CSS class from a string of CSS classes
    """
    remove = set(split_css_classes(css_class))
    classes_list = [c for c in split_css_classes(css_classes)
                    if c not in remove]
    return ' '.join(classes_list)


def render_link_tag(url, rel='stylesheet', media=None):
    """
    Build a link tag
    """
    attrs = {
        'href': url,
        'rel': rel,
    }
    if media:
        attrs['media'] = media
    return render_tag('link', attrs=attrs, close=False)


def render_tag(tag, attrs=None, content=None, close=True):
    """
    Render a HTML tag
    """
    builder = '<{tag}{attrs}>{content}'
    if content or close:
        builder += '</{tag}>'
    return format_html(
        builder,
        tag=tag,
        attrs=mark_safe(flatatt(attrs)) if attrs else '',
        content=text_value(content),
    )


def render_template_file(template, context=None):
    """
    Render a Template to unicode
    """
    assert isinstance(context, Mapping)
    template = get_template(template)
    return template.render(context)


def url_replace_param(url, name, value):
    """
    Replace a GET parameter in an URL
    """
    url_components = urlparse(force_str(url))
    query_params = parse_qs(url_components.query)
    query_params[name] = value
    query = urlencode(query_params, doseq=True)
    return force_text(urlunparse([
        url_components.scheme,
        url_components.netloc,
        url_components.path,
        url_components.params,
        query,
        url_components.fragment,
    ]))
