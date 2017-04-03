from django.template import RequestContext
from django.shortcuts import render_to_response


def demo(request):
    return render_to_response("demo.html", {}, RequestContext(request))
