# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


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
                ('date_initial_validity', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_end_validity', models.DateTimeField(default=django.utils.timezone.now)),
                ('views', models.PositiveIntegerField(default=0, editable=False)),
                ('status', models.SmallIntegerField(default=1, choices=[(1, b'Active'), (2, b'Archived'), (3, b'Deleted')])),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
