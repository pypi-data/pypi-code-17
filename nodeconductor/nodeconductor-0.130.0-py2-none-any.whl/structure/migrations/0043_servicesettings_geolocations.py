# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-01 09:29
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0042_add_service_certification_homepage_and_terms'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicesettings',
            name='geolocations',
            field=jsonfield.fields.JSONField(blank=True, default=[], help_text='List of latitudes and longitudes. For example: [{"latitude": 123, "longitude": 345}, {"latitude": 456, "longitude": 678}]'),
        ),
    ]
