# -*- coding: utf-8 -*-

from os import path
from cromlech.browser import IRenderable
from cromlech.i18n import ILanguage
from dolmen.breadcrumbs import breadcrumbs
from dolmen.template import TALTemplate
from zope.interface import implementer


TEMPLATES_DIR = path.join(path.dirname(__file__), 'templates')
template = TALTemplate(path.join(TEMPLATES_DIR, 'breadcrumbs.pt'))


def render_breadcrumbs(renderer, crumbs, separator="&rarr;"):
    namespace = dict(
        breadcrumbs=crumbs,
        target_language=ILanguage(renderer.request, None),
        separator=separator)
    return template.render(renderer, **namespace)


@implementer(IRenderable)
class BreadcrumbsRenderer(object):

    resolver = None
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def update(self):
        self.breadcrumbs = list(
            breadcrumbs(self.context, self.request, self.resolver))

    def render(self):
        return render_breadcrumbs(self, self.breadcrumbs)
