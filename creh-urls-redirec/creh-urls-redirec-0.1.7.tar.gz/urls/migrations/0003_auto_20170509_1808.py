# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('urls', '0002_auto_20170509_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlredirect',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 9, 23, 8, 56, 784279, tzinfo=utc), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlredirect',
            name='date_end_validity',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 9, 23, 8, 56, 784221, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlredirect',
            name='date_initial_validity',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 9, 23, 8, 56, 784193, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlredirect',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 9, 23, 8, 56, 784299, tzinfo=utc), editable=False),
            preserve_default=True,
        ),
    ]
