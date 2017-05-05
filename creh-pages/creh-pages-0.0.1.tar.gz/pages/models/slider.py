# -*- coding: utf-8 -*-
from django.db import models
from imagekit.models import ImageSpecField

from pages.utils.database import AuditableMixin
from pages.utils.image import get_slider_sizes
from pages.managers import SliderManager
from pages.utils import constants


class Slider(AuditableMixin):

    page = models.ForeignKey('Page')

    title = models.CharField(
        max_length=200,
    )

    is_active = models.BooleanField(
        default=False
    )

    dots = models.BooleanField(
        default=False
    )

    speed = models.IntegerField(
        default=500
    )

    objects = SliderManager()

    def __str__(self):
        return "({}) {}".format(self.title, self.title)

    class Meta:
        db_table = 'sliders'


class SliderItem(AuditableMixin):

    slider = models.ForeignKey('Slider')

    picture = ImageSpecField(
        source='slider_image',
        processors=get_slider_sizes(),
        format=constants.PAGE_SLIDER_FORMAT,
        options=constants.PAGE_SLIDER_OPTIONS,
    )

    is_active = models.BooleanField(
        default=False
    )

    active_from = models.DateTimeField()

    active_to = models.DateTimeField()

    order = models.SmallIntegerField(
        default=1
    )

    def __str__(self):
        return "({}) {}".format(self.slider, self.picture)

    class Meta:
        db_table = 'slider_items'


class SliderContentType(models.Model):

    name = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'slider_content_types'


class SliderContent(models.Model):

    type_content = models.ForeignKey('SliderContentType')

    content = models.TextField()

    config = models.TextField()

    order = models.SmallIntegerField(
        default=1
    )

    def __str__(self):
        return "({}) {}".format(self.name, self.title)

    class Meta:
        db_table = 'slider_contents'

