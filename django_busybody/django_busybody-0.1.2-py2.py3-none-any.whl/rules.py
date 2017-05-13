# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db.models.signals import pre_save, post_init
from . import easy_crypto


def _encrypt(fields, sender, instance, **kwargs):
    for field in fields:
        if not hasattr(instance, field):
            continue
        setattr(instance, field, easy_crypto.aes_encrypt(getattr(instance, field)))


def _decrypt(fields, sender, instance, **kwargs):
    if not instance.pk:
        return
    for field in fields:
        if not hasattr(instance, field):
            continue
        try:
            setattr(instance, field, easy_crypto.aes_decrypt(getattr(instance, field)))
        except TypeError:
            pass


def encrypt_field(klass, field_name):
    encrypt_fields(klass, [field_name])


def encrypt_fields(klass, field_names):
    name = '_'.join(field_names)
    pre_save.connect(
        lambda *args, **kwargs: _encrypt(field_names, *args, **kwargs),
        klass,
        dispatch_uid='django_busybody.rules.encrypt_{}_{}'.format(klass, name))

    post_init.connect(
        lambda *args, **kwargs: _decrypt(field_names, *args, **kwargs),
        klass,
        dispatch_uid='django_busybody.rules.decrypt_{}_{}'.format(klass, name))

