# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0002_log_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='location',
            field=models.CharField(max_length=300, null=True),
            preserve_default=True,
        ),
    ]
