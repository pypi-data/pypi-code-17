from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect

from djprogress.models import Progress
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.utils.translation import ugettext as _

import json
import datetime

@staff_member_required
def overview(request):
    progresses = Progress.objects.order_by('pk')
    context = {'progresses': progresses}
    return render_to_response('djprogress/overview.html', context, context_instance=RequestContext(request))

@staff_member_required
def api_get_progress(request):
    name = request.GET.get('name', u'')
    progresses = Progress.objects.filter(name=name)
    if progresses:
        progress = progresses[0]
        seconds_left = progress.eta and (progress.eta - datetime.datetime.now()).seconds or -1
        context = {'current': progress.current, 'total': progress.total, 'seconds_left': seconds_left}
        return HttpResponse(json.dumps(context, indent=2))
    else:
        context = {'current': 100, 'total': 100, 'seconds_left': 0}
        return HttpResponse(json.dumps(context, indent=2))

@staff_member_required
def show_exception(request, progress_id):
    progress = get_object_or_404(Progress, pk=progress_id)
    return HttpResponse(progress.exception)

@staff_member_required
def resolve(request, progress_id):
    progress = get_object_or_404(Progress, pk=progress_id)
    while progress.parent:
        progress = progress.parent
    progress.delete()
    messages.success(request, _(u'Marked progress "%s" as resolved.') % progress.name)
    return redirect(reverse('djprogress_overview'))
