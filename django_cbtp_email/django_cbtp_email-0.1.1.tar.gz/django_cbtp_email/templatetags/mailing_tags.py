# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

import io

from django.contrib.staticfiles import finders
from django.template import Library
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from django_cbtp_email.errors import CssForEmailNotFoundError

register = Library()


@register.simple_tag()
def css_direct(css_path):
    """
    :type css_path: str
    """
    if not css_path.endswith(".css"):
        raise ValueError("c")

    result = finders.find(css_path)

    if not result:
        raise CssForEmailNotFoundError(
            "Cannot find \"{}\", searched locations: {}".format(css_path, finders.searched_locations))

    with io.open(result, mode="rt", encoding="utf-8") as the_file:  # rt == read text mode
        css_content = the_file.read()

    css_style = "<style type=\"text/css\">{0}</style>".format(css_content)

    return mark_safe(css_style)


@register.simple_tag(takes_context=True)
def static_direct(context, static_path):
    """
    :type static_path: basestring, str
    """
    if "request" in context:
        return static(static_path)

    return "file:///{}".format(finders.find(static_path))
