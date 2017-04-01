# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-13 14:29
from __future__ import unicode_literals

from django.db import migrations, models


def set_order_dates(apps, schema_editor):
    Article = apps.get_model('cms_articles', 'Article')

    for article in Article.objects.all():
        article.order_date = article.publication_date or article.creation_date
        article.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cms_articles', '0005_attributes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('-order_date',), 'permissions': (('publish_article', 'Can publish page'),), 'verbose_name': 'article', 'verbose_name_plural': 'articles'},
        ),
        migrations.AddField(
            model_name='article',
            name='order_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.RunPython(set_order_dates),
        migrations.AlterField(
            model_name='article',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='publication or creation time'),
        ),
    ]
