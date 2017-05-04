# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, db_index=True)),
                ('current', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=100)),
                ('eta', models.DateTimeField(null=True, blank=True)),
                ('last_updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('exception', models.TextField(blank=True)),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='djprogress.Progress', null=True)),
            ],
            options={
                'verbose_name': 'progress',
                'verbose_name_plural': 'progresses',
            },
            bases=(models.Model,),
        ),
    ]
