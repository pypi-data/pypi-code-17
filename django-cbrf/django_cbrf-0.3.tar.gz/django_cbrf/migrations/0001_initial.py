# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 09:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cbrf_id', models.CharField(db_index=True, max_length=12, unique=True, verbose_name='CB RF code')),
                ('parent_code', models.CharField(max_length=6, verbose_name='parent code')),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('eng_name', models.CharField(max_length=64, verbose_name='english name')),
                ('denomination', models.SmallIntegerField(default=1, verbose_name='denomination')),
                ('iso_num_code', models.SmallIntegerField(blank=True, default=None, null=True, verbose_name='ISO numeric code')),
                ('iso_char_code', models.CharField(blank=True, db_index=True, default=None, max_length=3, null=True, verbose_name='ISO char code')),
            ],
            options={
                'verbose_name': 'currency',
                'verbose_name_plural': 'currencies',
                'ordering': ('cbrf_id',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('value', models.DecimalField(decimal_places=4, max_digits=9, verbose_name='value')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='django_cbrf_record', to='django_cbrf.Currency')),
            ],
            options={
                'verbose_name': 'record',
                'verbose_name_plural': 'records',
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='record',
            unique_together=set([('date', 'currency')]),
        ),
    ]
