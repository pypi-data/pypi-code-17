# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

import logging
import os
from abc import ABCMeta

import six

from .mail_funcs import send_mail

logger = logging.getLogger(__name__)


class Mailer(object):
    __metaclass__ = ABCMeta

    template = None
    context = {}
    to = None
    subject = None
    attachment = None

    def __init__(self, **kwargs):
        """
        Constructor. Called in the URLconf; can contain helpful extra
        keyword arguments, and other things.
        """
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)

    def log_send_mail_error(self, exception_to_log):
        logger.error(exception_to_log,
                     extra={
                         'stack': True,
                         'data': {
                             'self': self,
                         }
                     }
                     )

    def attach_file(self, file_path):
        if not os.path.isfile(file_path):
            raise ValueError("\"{}\" is not a valid file".format(file_path))

        self.attachment = file_path

    def send_message(self):
        to = self.get_recipients()

        try:
            send_mail(
                self.subject,
                self.template,
                context=self.context,
                to=to,
                attachment=self.attachment
            )
        except Exception as ex:
            self.log_send_mail_error(ex)
            raise

    def get_recipients(self):
        if not self.to:
            raise ValueError("Recipient of e-mail is not set.")

        return self.to if hasattr(self.to, '__iter__') else [self.to]
