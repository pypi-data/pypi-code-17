# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yamoney', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044f', blank=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='fathersname',
            field=models.CharField(max_length=255, verbose_name='\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044f', blank=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='firstname',
            field=models.CharField(max_length=255, verbose_name='\u0418\u043c\u044f \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044f', blank=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='lastname',
            field=models.CharField(max_length=255, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044f', blank=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='phone',
            field=models.CharField(max_length=50, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044f', blank=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='test_notification',
            field=models.BooleanField(default=False, verbose_name='\u0422\u0435\u0441\u0442\u043e\u0432\u0430\u044f \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u044f'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='unaccepted',
            field=models.BooleanField(default=True, help_text='\u041f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044e \u043d\u0443\u0436\u043d\u043e \u043e\u0441\u0432\u043e\u0431\u043e\u0434\u0438\u0442\u044c \u043c\u0435\u0441\u0442\u043e \u0432 \u043a\u043e\u0448\u0435\u043b\u044c\u043a\u0435 \u0438\u043b\u0438 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u044c \u043a\u043e\u0434 \u043f\u0440\u043e\u0442\u0435\u043a\u0446\u0438\u0438', verbose_name='\u041f\u0435\u0440\u0435\u0432\u043e\u0434 \u043d\u0435 \u0437\u0430\u0447\u0438\u0441\u043b\u0435\u043d'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(verbose_name='\u0421\u0443\u043c\u043c\u0430, \u043a\u043e\u0442\u043e\u0440\u0430\u044f \u0437\u0430\u0447\u0438\u0441\u043b\u0435\u043d\u0430 \u043d\u0430 \u0441\u0447\u0435\u0442 \u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044f', max_digits=18, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='codepro',
            field=models.BooleanField(default=False, verbose_name='\u0421\u043b\u0443\u0436\u0435\u0431\u043d\u043e\u0435'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='withdraw_amount',
            field=models.DecimalField(null=True, verbose_name='\u0421\u0443\u043c\u043c\u0430, \u043a\u043e\u0442\u043e\u0440\u0430\u044f \u0441\u043f\u0438\u0441\u0430\u043d\u0430 \u0441\u043e \u0441\u0447\u0435\u0442\u0430 \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044f', max_digits=18, decimal_places=2, blank=True),
        ),
    ]
