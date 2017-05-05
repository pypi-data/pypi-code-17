# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone


class SEOMixin(models.Model):

    seo_title = models.CharField(
        max_length=100,
    )

    seo_sub_title = models.CharField(
        max_length=100,
    )

    seo_desc = models.CharField(
        max_length=100,
    )

    seo_keywords = models.CharField(
        max_length=100,
    )

    class Meta:
        abstract = True


class AuditableMixin(models.Model):

    created = models.DateTimeField(
        default=timezone.now,
    )

    modified = models.DateTimeField(
        default=timezone.now,
    )

    class Meta:
        abstract = True
