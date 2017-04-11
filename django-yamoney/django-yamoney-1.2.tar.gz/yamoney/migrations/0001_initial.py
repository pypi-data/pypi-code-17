# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notification_type', models.CharField(max_length=100, verbose_name='\u0422\u0438\u043f \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u0438', choices=[(b'p2p-incoming', '\u041f\u0435\u0440\u0435\u0432\u043e\u0434 \u0438\u0437 \u043a\u043e\u0448\u0435\u043b\u044c\u043a\u0430'), (b'card-incoming', '\u041f\u0435\u0440\u0435\u0432\u043e\u0434 \u0441 \u043a\u0430\u0440\u0442\u044b')])),
                ('operation_id', models.CharField(max_length=255, verbose_name='\u0418\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u0438')),
                ('amount', models.FloatField(verbose_name='\u0421\u0443\u043c\u043c\u0430, \u043a\u043e\u0442\u043e\u0440\u0430\u044f \u0437\u0430\u0447\u0438\u0441\u043b\u0435\u043d\u0430 \u043d\u0430 \u0441\u0447\u0435\u0442 \u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044f')),
                ('withdraw_amount', models.FloatField(null=True, verbose_name='\u0421\u0443\u043c\u043c\u0430, \u043a\u043e\u0442\u043e\u0440\u0430\u044f \u0441\u043f\u0438\u0441\u0430\u043d\u0430 \u0441\u043e \u0441\u0447\u0435\u0442\u0430 \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044f', blank=True)),
                ('currency', models.CharField(default=b'643', max_length=100, verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430', choices=[(b'643', '\u0440\u0443\u0431.')])),
                ('datetime', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u0441\u043e\u0432\u0435\u0440\u0448\u0435\u043d\u0438\u044f \u043f\u0435\u0440\u0435\u0432\u043e\u0434\u0430')),
                ('sender', models.CharField(help_text='\u0422\u043e\u043b\u044c\u043a\u043e \u0434\u043b\u044f \u043f\u0435\u0440\u0435\u0432\u043e\u0434\u043e\u0432 \u0438\u0437 \u043a\u043e\u0448\u0435\u043b\u044c\u043a\u0430', max_length=255, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0441\u0447\u0435\u0442\u0430 \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044f', blank=True)),
                ('codepro', models.BooleanField(verbose_name='\u0421\u043b\u0443\u0436\u0435\u0431\u043d\u043e\u0435')),
                ('label', models.CharField(max_length=255, verbose_name='\u041c\u0435\u0442\u043a\u0430 \u043f\u043b\u0430\u0442\u0435\u0436\u0430', blank=True)),
            ],
            options={
                'verbose_name': '\u041f\u0435\u0440\u0435\u0432\u043e\u0434',
                'verbose_name_plural': '\u041f\u0435\u0440\u0435\u0432\u043e\u0434\u044b',
            },
        ),
    ]
