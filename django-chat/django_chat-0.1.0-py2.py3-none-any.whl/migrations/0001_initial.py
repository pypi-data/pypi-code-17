# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('message', models.TextField(verbose_name='Message')),
                ('created_at', models.DateTimeField(verbose_name='Created date', default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
        migrations.CreateModel(
            name='MessageDelivery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('delivered_at', models.DateTimeField(verbose_name='Message delivery date', blank=True, null=True)),
                ('message', models.ForeignKey(verbose_name='Message', related_name='deliveries', to='chat.Message')),
                ('receiver', models.ForeignKey(verbose_name='Message receiver', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Message delivery',
                'verbose_name_plural': 'Messages delivery',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Room name', max_length=255)),
                ('created_at', models.DateTimeField(verbose_name='Created date', default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(verbose_name='Room creator', blank=True, db_column='created_by', related_name='my_chat_rooms', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(verbose_name='Room users', related_name='chat_rooms', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.ForeignKey(verbose_name='Room', related_name='messages', to='chat.Room'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(verbose_name='Message author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterIndexTogether(
            name='room',
            index_together=set([('name',)]),
        ),
    ]
