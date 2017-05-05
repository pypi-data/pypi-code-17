# -*- coding: utf-8 -*-
from django.db import models

from pages.utils.database import SEOMixin, AuditableMixin, ActivatedMixin, ActivatedQuerySet


class CustomQuerySet(ActivatedQuerySet):

    def get_queryset(self):
        return ActivatedQuerySet(self.model, using=self._db)


class Page(SEOMixin, AuditableMixin, ActivatedMixin):

    title = models.CharField(
        max_length=100,
    )

    slug = models.SlugField(
        max_length=150,
    )

    external_url = models.URLField(
        verbose_name='External URL',
        max_length=500,
        blank=True,
    )

    objects = CustomQuerySet.as_manager()

    def __str__(self):
        return "({}) {}".format(self.title, self.title)

    class Meta:
        db_table = 'pages'
