# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.mail import mail_admins
from .forms import YandexNotificationForm
from .conf import settings


class NotificationView(CreateView):
    form_class = YandexNotificationForm
    http_method_names = ('post',)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationView, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        if settings.YAMONEY_MAIL_ADMINS_ON_TRANSACTION_ERROR:
            import json
            mail_admins(
                settings.YAMONEY_MAIL_ADMINS_ON_TRANSACTION_ERROR_SUBJECT,
                'Form data: \n{form_data}\n\nForm errors: \n{form_errors}'.format(
                    form_data=json.dumps(dict(self.request.POST), sort_keys=True, indent=4),
                    form_errors=form.errors.as_text()
                ),
            )
        return HttpResponseBadRequest()

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse()
