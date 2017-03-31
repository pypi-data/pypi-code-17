# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


class SendEmail(object):
    """
    Send an emails or several emails easily.

    **Example**
    ::
        email = SendEmail(
            to='user@example.com',
            template_name_suffix='recover-account',
            subject='Recover your account',
            is_html=True
        )
        email.set_from_email('no-reply@example.com')
        email.set_from_name('No Reply')
        email.add_context_data('protocol', 'https')
        email.add_context_data('domain', 'example.com')
        email.add_context_data('uid', uid)
        email.add_context_data('token', token)
        email.add_context_data('object', user)
        email.add_context_data('site_name', 'Boilerplate - Make it easy')
        email.send()
    """

    context_data = {}
    files = list()
    from_name = None
    from_email = None
    template_name = None

    def __init__(self, to, template_name_suffix, subject, is_html=False):
        if isinstance(to, list):
            self.to = to
        else:
            self.to = list()
            self.to.append(to)

        self.template_name_suffix = template_name_suffix
        self.subject = subject
        self.is_html = is_html

    def add_file(self, file):
        self.files.append(file)

    def add_context_data(self, key, value):
        """
        Add a key-value to the context data of the email

        **Parameters**:
            :key: A valid key name
            :value: Can be an object or any kind of value
        """
        self.context_data.update({
            str(key): value
        })

    def set_from_email(self, from_email=None):
        """
        Set the email sender

        **Parameters**:
            :from_email: String, a valid email
        """
        if from_email:
            self.from_email = str(from_email)
        else:
            self.from_email = settings.SERVER_EMAIL

    def set_from_name(self, from_name=None):
        """
        Set the name sender

        **Parameters**:
            :from_name: String, a valid name
        """
        if from_name:
            self.from_name = str(from_name)
        else:
            self.from_name = settings.SERVER_EMAIL

    def set_template_name_suffix(self, template_name_suffix=None):
        """
        Set the email template name suffix

        **Parameters**:
            :template_name_suffix: String: the name of the template without the extension
        """
        if template_name_suffix:
            self.template_name_suffix = str(template_name_suffix)

    def set_template_name(self, template_name=None):
        """
        Set the email template name

        **Parameters**:
            :template_name: String: the name of the template without the extension
        """
        if template_name:
            self.template_name = template_name
        else:
            if not self.template_name_suffix:
                self.set_template_name_suffix()

            self.template_name = 'mail/' + self.template_name_suffix

    def get_from_email(self):
        if not self.from_email:
            self.set_from_email()

        return self.from_email

    def get_from_name(self):
        if not self.from_name:
            self.set_from_name()

        return self.from_name

    def get_template_name_suffix(self):
        if not self.template_name_suffix:
            self.set_template_name_suffix()

        return self.template_name_suffix

    def get_template_name(self):
        if not self.template_name:
            self.set_template_name()

        return self.template_name

    def get_context_data(self, **kwargs):
        self.context_data.update({
            'email': self
        })

        return self.context_data

    def send(self, fail_silently=True, test=False):
        plain_template = get_template(self.get_template_name() + '.txt')
        plain_content = plain_template.render(self.get_context_data())

        if self.is_html:
            html_template = get_template(self.get_template_name() + '.html')
            html_content = html_template.render(self.get_context_data())

        if test:
            return plain_content

        msg = EmailMultiAlternatives(
            self.subject, plain_content,
            '%s <%s>' % (self.get_from_name(), self.get_from_email()),
            self.to
        )

        if self.is_html:
            msg.attach_alternative(html_content, 'text/html')

        if self.files:
            for name, file, content_type in self.files:
                msg.attach(name, file.read(), content_type)

        return msg.send(fail_silently=fail_silently)
