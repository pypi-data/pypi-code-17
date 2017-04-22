# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

import logging
import os

from annoying.functions import get_config
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import translation
from premailer import Premailer

logger = logging.getLogger(__name__)


def send_mail(subject, template, context, to, from_email=settings.DEFAULT_FROM_EMAIL,
              template_variant=get_config('DEFAULT_TEMPLATE_TYPE', 'html'), attachment=None):
    """
    Render template and send it as a mail.

    Usage:
        > ctx = { 'some_var': True }
        > send_mail('E-mail subject', 'default_file_extensiontension/emails/bar', context=ctx, to=['joh.doe@example.com'])
    """
    template_path = os.path.normcase("{}.{}".format(template, template_variant))
    current_language = translation.get_language()

    if isinstance(to, str):
        to = [to]

    try:
        # TODO Allow to activate different language
        translation.activate(current_language)
        html_message = render_to_string(template_path, context)
    finally:
        translation.activate(current_language)

    premailer = Premailer(
        html_message,
        base_url=get_config('BASE_URL_FOR_EMAIL_LINK', None),
        base_path=settings.STATIC_ROOT
    )

    html_message = premailer.transform()

    mail = EmailMessage(settings.EMAIL_SUBJECT_PREFIX + subject, html_message, to=to, from_email=from_email)
    if template_variant == "html":
        mail.content_subtype = "html"

    if attachment:
        mail.attach_file(attachment)

    mail.send()
