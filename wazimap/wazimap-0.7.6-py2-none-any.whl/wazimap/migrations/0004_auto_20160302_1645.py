# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-02 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wazimap', '0003_remove_geography_osm_area_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geography',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
    ]
