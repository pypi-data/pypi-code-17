# -*- coding: utf-8 -*-
import itertools

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
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
        return self.title

    class Meta:
        db_table = 'pages'


@receiver(pre_save, sender=Page)
def pre_save_page(sender, instance=None, **kwargs):
    instance.slug = orig = slugify(instance.title)

    for x in itertools.count(1):
        if not Page.objects.filter(slug=instance.slug).exists():
            break
        instance.slug = '%s-%d' % (orig, x)

    return instance