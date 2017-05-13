# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
# from six import reraise as raise_
# from __future__ import division
# from builtins import bytes
# from future.utils import python_2_unicode_compatible
# @python_2_unicode_compatible
import logging
import traceback

from django.conf import settings
from django.utils.module_loading import import_string

from .. import models


logger = logging.getLogger(__name__)


class LogEmailBackend(object):
    """
    A wrapper around the SMTP backend that logs all emails to the DB.
    settings.EMAIL_BACKEND_ORG is actual email backend.
    """

    def __init__(self, *args, **kwarg):
        self.__dict__['_upper_'] = import_string(settings.EMAIL_BACKEND_ORG)(*args, **kwarg)

    def __getattr__(self, key):
        return getattr(self.__dict__['_upper_'], key)

    def __setattr__(self, key, value):
        return setattr(self.__dict__['_upper_'], key, value)

    def send_messages(self, email_messages):
        """
        A helper method that does the actual logging
        """
        created = []
        try:
            for email_message in email_messages:
                email_record = models.Email.objects.create(
                    to='; '.join(email_message.recipients()),
                    subject=email_message.subject, body=email_message.body,
                )
                created.append(email_record)
        except:
            logger.exception("Error creating email object")
            created = []

        try:
            result = self._upper_.send_messages(email_messages)
            for index, email in enumerate(email_messages):
                email_record = created[index]
                email_record.status = email.extra_headers.get('status', 0)
                email_record.message_id = email.extra_headers.get('message_id', None)
                email_record.request_id = email.extra_headers.get('request_id', None)
                email_record.category = getattr(email, '_category', None)
                email_record.save()
            return result
        except:
            stack_trace = traceback.format_exc()
            for record in created:
                record.stack_trace = stack_trace
                record.ok = False
                record.save()
            raise

        return True
