# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "rmd/about.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AboutView, self).get_context_data(**kwargs)

        from assetadapter.version import __version__ as assetadapter_version
        from orchestrator.version import __version__ as orchestrator_version
        from processengine.version import __version__ as processengine_version
        from rmd.version import __version__ as rmd_version

        context['assetadapter_version'] = assetadapter_version
        context['orchestrator_version'] = orchestrator_version
        context['processengine_version'] = processengine_version
        context['rmd_version'] = rmd_version

        return context