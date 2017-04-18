# -*- coding: utf-8 -*-

import urllib
from cromlech.browser import IPublicationRoot
from dolmen.location import get_absolute_url, lineage_chain


_safe = '@+'  # Characters that we don't want to have quoted


def resolve_name(item):
    """Choose a display name for the current context.
    This method has been splitted out for convenient overriding.
    """
    name = getattr(item, '__name__', None)
    if name is None and not IPublicationRoot.providedBy(item):
        raise KeyError('Object name (%r) could not be resolved.' % item)
    return name, name


def breadcrumbs(item, request, resolver=resolve_name):
    if resolver is None:
        resolver = resolve_name
    kin = lineage_chain(item)
    if kin:
        kin.reverse()
        root = kin.pop(0)
        base_url = get_absolute_url(root, request)
        name, title = resolver(root)
        yield {'name': title, 'url': base_url}

        for sibling in kin:
            name, title = resolver(sibling)
            base_url += '/' + urllib.quote(name.encode('utf-8'), _safe)
            yield {'name': title, 'url': base_url}
