#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)

import logging
import re

from classytags.arguments import Argument, MultiKeywordArgument, MultiValueArgument
from classytags.core import Tag, Options
from classytags.utils import NULL
from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template import Library

register = Library()
logger = logging.getLogger(__name__)


class MultiKeywordOrValueArgument(MultiKeywordArgument):
    def parse(self, parser, token, tagname, kwargs):
        key, value = self.parse_token(parser, token)

        only_arg_given = key is NULL

        if self.name in kwargs:
            if only_arg_given and not isinstance(kwargs.get(self.name), list) or not only_arg_given and not isinstance(kwargs.get(self.name), dict):
                raise template.TemplateSyntaxError(
                    "Don't mix *args and **kwargs in call to reverse()!"
                )

        if only_arg_given:
            return self.handle_as_arg(value, kwargs)
        else:
            return self.handle_as_kwarg(key, value, kwargs)

    def handle_as_arg(self, value, kwargs):
        if self.name in kwargs:
            if self.max_values and len(kwargs[self.name]) == self.max_values:
                return False
            kwargs[self.name].append(value)
        else:
            kwargs[self.name] = MultiValueArgument.sequence_class(value)

        return True

    def handle_as_kwarg(self, key, value, kwargs):
        if self.name in kwargs:
            if self.max_values and len(kwargs[self.name]) == self.max_values:
                return False
            kwargs[self.name][key] = value
        else:
            kwargs[self.name] = self.wrapper_class({
                key: value
            })

        return True


def is_current(pattern_or_urlname, path, view_args, view_kwargs):
    """
    Check if given :path is active :pattern_or_urlname.
    Credits: http://stackoverflow.com/a/18772289/752142

    :type pattern_or_urlname: unicode
    :type path: unicode
    :type view_args: list
    :type view_kwargs: dict
    :rtype: bool
    """
    if view_args and view_kwargs:
        logger.warning("args and kwargs given")

    try:
        pattern = reverse(pattern_or_urlname, args=view_args, kwargs=view_kwargs)
    except NoReverseMatch as e:
        # Given pattern_or_urlname is not urlname
        pattern = pattern_or_urlname

    pattern = '^' + pattern + "$"  # Strict checking

    if re.search(pattern, path):
        return True  # This view/pattern IS active!
    else:
        return False  # NOT active


class IsActiveClassyTag(Tag):
    name = 'isactive'
    options = Options(
        Argument('pattern_or_urlname', required=True, resolve=True),
        MultiKeywordOrValueArgument('view_data', required=False, resolve=True),
        blocks=[('else', 'pre_else'), ('endisactive', 'post_else')],
    )

    # noinspection PyMethodOverriding
    def render_tag(self, context, pattern_or_urlname, view_data, pre_else, post_else):
        """
        :type context: dict
        :type pattern_or_urlname: unicode
        :type view_data: list|dict
        :type pre_else: django.template.base.NodeList
        :type post_else: django.template.base.NodeList
        """
        path = context.get('request').path
        is_args = isinstance(view_data, list)
        view_args = view_data if is_args and view_data else []
        view_kwargs = view_data if not is_args and view_data else {}

        is_view_active = is_current(pattern_or_urlname, path, view_args, view_kwargs)

        if is_view_active:
            output = pre_else.render(context)
        else:
            output = post_else.render(context)

        return output


register.tag(IsActiveClassyTag)
