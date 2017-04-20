# -*- coding: utf-8 -*-
import re
from postman_client.exceptions import InvalidParam


class Mail(object):
    TRACK_EMAIL_REGEX = re.compile(r"<.*?(.*).*>")
    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")

    def __init__(self, **kwargs):
        assert 'from_email' in kwargs or ('use_template_email' in kwargs and kwargs['use_template_email']), \
            'Please provide an reply email'
        assert 'recipient_list' in kwargs and len(kwargs.get('recipient_list')), \
            'Impossible to send email without any recipient'
        assert 'subject' in kwargs or ('use_template_subject' in kwargs and kwargs['use_template_subject']), \
            'Impossible to send email without a subject'

        # General mail vars
        self.set_attr('tags', kwargs)
        self.set_attr('subject', kwargs)
        self.set_attr('from_name', kwargs)
        self.set_attr('from_email', kwargs)
        self.set_attr('message_text', kwargs)
        self.set_attr('message_html', kwargs)
        self.set_attr('recipient_list', kwargs)
        self.check_recipient_list()
        self.set_attr('activate_tracking', kwargs)
        self.set_attr('get_text_from_html', kwargs)
        # self.set_attr('expose_recipients_list', kwargs)

        # Template mail vars
        self.set_attr('headers', kwargs)
        self.set_attr('context', kwargs)
        self.set_attr('template_name', kwargs)
        self.set_attr('use_template_from', kwargs)
        self.set_attr('use_template_email', kwargs)
        self.set_attr('use_template_subject', kwargs)
        self.set_attr('context_per_recipient', kwargs)

    def set_attr(self, attr, kwargs):
        if attr in kwargs:
            setattr(self, attr, kwargs.get(attr))

    def __track_email(self, value):
        tracked = self.TRACK_EMAIL_REGEX.search(value)
        if tracked:
            return tracked.group(1)
        return None

    def __validate_email(self, email):
        valid = self.EMAIL_REGEX.match(email)
        return valid is not None

    def __validate_recipient(self, value):
        email = self.__track_email(value)
        return email and self.__validate_email(email)

    def check_recipient_list(self):
        exception_reason = "Expected format ('Name <email>'; or '<email>') wasn't matched"
        for recipient in getattr(self, 'recipient_list'):
            if not self.__validate_recipient(recipient):
                raise InvalidParam(
                    message_values=("'recipient_list'", exception_reason)
                )

    @staticmethod
    def __mount_param_from(payload):
        payload['from'] = ''
        if 'from_name' in payload and payload['from_name']:
            payload['from'] += payload['from_name']
            del payload['from_name']
        if 'from_email' in payload and payload['from_email']:
            payload['from'] += ' <{0}>'.format(payload['from_email'])
            del payload['from_email']
        return payload['from'].strip()

    def get_payload(self):
        payload = self.__dict__
        payload['from'] = Mail.__mount_param_from(payload)
        payload['sended_by'] = 4

        return payload
