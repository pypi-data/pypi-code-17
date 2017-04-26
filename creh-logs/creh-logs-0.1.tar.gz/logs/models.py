# -*- coding: utf-8 -*-
from . import contstants

from django.db import models
from django.utils import timezone


class Log(models.Model):

    title = models.CharField(
        max_length=500,
    )

    message = models.TextField()

    code_error = models.CharField(
        max_length=3,
        choices=contstants.CODE_CHOICES,
        null=True
    )

    level = models.SmallIntegerField(
        choices=contstants.LEVEL_CHOICES,
        default=contstants.LEVEL_INFO
    )

    status = models.SmallIntegerField(
        choices=contstants.STATUS_CHOICES,
        default=contstants.STATUS_ACTIVE
    )

    location = models.CharField(
        max_length=300,
    )

    tag = models.CharField(
        max_length=50,
        null=True
    )

    created_at = models.DateTimeField(
        default=timezone.now,
    )

    updated_at = models.DateTimeField(
        default=timezone.now,
    )

    def __str__(self):
        return "({}) {}".format(self.display_level(), self.title)