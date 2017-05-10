# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('urls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='urlredirect',
            name='status',
        ),
        migrations.AddField(
            model_name='urlredirect',
            name='is_active',
            field=models.SmallIntegerField(default=1, choices=[(1, b'True'), (2, b'False')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='urlredirect',
            name='is_permanent',
            field=models.SmallIntegerField(default=1, choices=[(1, b'True'), (2, b'False')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlredirect',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 9, 23, 7, 28, 392190, tzinfo=utc), editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlredirect',
            name='date_end_validity',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 9, 23, 7, 28, 392118, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlredirect',
            name='date_initial_validity',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 9, 23, 7, 28, 392077, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlredirect',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 9, 23, 7, 28, 392216, tzinfo=utc), editable=False),
            preserve_default=True,
        ),
    ]
