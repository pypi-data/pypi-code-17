from django.template import RequestContext
from django.shortcuts import render


def quick_response(request, template, context={}):
    return render(request, template, context)
