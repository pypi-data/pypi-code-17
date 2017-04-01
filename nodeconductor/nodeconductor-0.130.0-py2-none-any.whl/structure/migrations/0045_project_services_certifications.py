# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-17 10:50
from __future__ import unicode_literals

from django.db import migrations, models

import nodeconductor.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0044_terms_of_services_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='certifications',
            field=models.ManyToManyField(blank=True, related_name='projects', to='structure.ServiceCertification'),
        ),
        migrations.AlterField(
            model_name='servicecertification',
            name='name',
            field=models.CharField(max_length=150, unique=True, validators=[nodeconductor.core.validators.validate_name], verbose_name='name'),
        ),
    ]
