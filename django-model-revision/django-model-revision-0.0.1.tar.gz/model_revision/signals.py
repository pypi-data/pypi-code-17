# -*- coding: utf-8 -*-
from model_revision.models import Revision


def pre_save_callback(sender, **kwargs):
    instance = kwargs['instance']
    raw = kwargs['raw']
    if instance.pk and not raw:
        Revision.objects.create_from_instance(instance.__class__.objects.get(pk=instance.pk))
