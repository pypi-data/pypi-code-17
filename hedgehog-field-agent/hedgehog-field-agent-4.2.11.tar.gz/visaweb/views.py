# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from orchestrator.version import __version__
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
# @permission_classes((permissions.AllowAny,))
def index(request):
    context = {
        'shell': 'visaweb/src/hedgehog-app.html',
        'service_worker': 'visaweb/service-worker.js',
        'webcomponents': 'visaweb/bower_components/webcomponentsjs/webcomponents-lite.min.js',
        'shell_element': 'hedgehog-app',
        'version': __version__
    }
    return render(request, template_name='visaweb/index.html', context=context)