# -*- coding: utf-8 -*-

import venusian
from pyramid.httpexceptions import HTTPMethodNotAllowed


def add_class_view(config, view_class, **kwargs):
    u'''
    '''

    def wrapped(context, request):
        view = view_class()
        method = request.method.lower()
        allowed_methods = getattr(view, 'allowed_options', None)
        if allowed_methods is not None and method not in allowed_methods:
            raise HTTPMethodNotAllowed()
        view_method = getattr(view, method, None)
        if view_method is None:
            raise HTTPMethodNotAllowed()
        return view_method(context, request)

    config.add_view(wrapped, **kwargs)


def add_resource_view(config, view_class):
    u'''
    '''
    pass


class class_view_config(object):
    u'''
    '''

    venusian = venusian  # for testing injection

    def __init__(self, **settings):
        if 'for_' in settings:
            if settings.get('context') is None:
                settings['context'] = settings['for_']
        self.__dict__.update(settings)

    def __call__(self, wrapped):
        settings = self.__dict__.copy()
        depth = settings.pop('_depth', 0)

        def callback(context, name, ob):
            config = context.config.with_package(info.module)
            config.add_class_view(ob, **settings)

        info = self.venusian.attach(wrapped, callback, category='pyramid', depth=depth + 1)

        if info.scope == 'class':
            # if the decorator was attached to a method in a class, or
            # otherwise executed at class scope, we need to set an
            # 'attr' into the settings if one isn't already in there
            if settings.get('attr') is None:
                settings['attr'] = wrapped.__name__

        settings['_info'] = info.codeinfo  # fbo "action_method"
        return wrapped


class resource_view_config(object):
    u'''
    '''
    pass


def includeme(config):
    config.add_directive('add_class_view', add_class_view)
    config.add_directive('add_resource_view', add_resource_view)
