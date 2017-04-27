# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import permissions
from rest_framework.decorators import permission_classes

from orchestrator.version import __version__
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token, ensure_csrf_cookie


@ensure_csrf_cookie
def index(request):
    context = {
        'shell': 'visaweb/src/hedgehog-app.html',
        'service_worker': 'visaweb/service-worker.js',
        'webcomponents': 'visaweb/bower_components/webcomponentsjs/webcomponents-lite.min.js',
        'shell_element': 'hedgehog-app',
        'version': __version__
    }
    return render(request, template_name='visaweb/index.html', context=context)