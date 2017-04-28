# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('message', models.TextField()),
                ('code_error', models.CharField(max_length=3, null=True, choices=[(b'400', b'Bad Request'), (b'401', b'Unauthorized'), (b'403', b'Forbidden'), (b'404', b'Not Found'), (b'405', b'Method Not Allowed'), (b'406', b'Not Acceptable'), (b'407', b'Proxy Authentication Required'), (b'408', b'Request Timeout'), (b'409', b'Conflict'), (b'410', b'Gone'), (b'411', b'Length Required'), (b'412', b'Precondition Failed'), (b'413', b'Request Entity Too Large'), (b'414', b'Request-URI Too Long'), (b'415', b'Unsupported Media Type'), (b'416', b'Requested Range Not Satisfiable'), (b'417', b'Expectation Failed'), (b'418', b'I am a teapot'), (b'422', b'Unprocessable Entity (WebDAV - RFC 4918)'), (b'423', b'Locked (WebDAV - RFC 4918)'), (b'424', b'Failed Dependency (WebDAV) (RFC 4918)'), (b'425', b'Unassigned'), (b'426', b'Upgrade Required (RFC 7231)'), (b'428', b'Precondition Required'), (b'429', b'Too Many Requests'), (b'431', b'Request Header Fileds Too Large)'), (b'449', b'Argument not optional'), (b'451', b'Unavailable for Legal Reasons')])),
                ('level', models.SmallIntegerField(default=2, choices=[(1, b'Error'), (2, b'Info'), (3, b'Warning')])),
                ('status', models.SmallIntegerField(default=1, choices=[(1, b'Active'), (2, b'Archived'), (3, b'Deleted')])),
                ('location', models.CharField(max_length=300)),
                ('tag', models.CharField(max_length=50, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
