# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UrlRedirect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url_source', models.TextField(unique=True)),
                ('url_destination', models.TextField()),
                ('date_initial_validity', models.DateTimeField(default=datetime.datetime(2017, 5, 7, 5, 28, 0, 415369, tzinfo=utc))),
                ('date_end_validity', models.DateTimeField(default=datetime.datetime(2017, 5, 7, 5, 28, 0, 415404, tzinfo=utc))),
                ('views', models.PositiveIntegerField(default=0, editable=False)),
                ('status', models.SmallIntegerField(default=1, choices=[(1, b'Active'), (2, b'Archived'), (3, b'Deleted')])),
                ('created_at', models.DateTimeField(default=datetime.datetime(2017, 5, 7, 5, 28, 0, 415460, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2017, 5, 7, 5, 28, 0, 415481, tzinfo=utc), editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
