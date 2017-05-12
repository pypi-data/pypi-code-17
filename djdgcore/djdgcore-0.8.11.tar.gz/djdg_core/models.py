#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author lilx
created on 2017/5/12
 """
from __future__ import unicode_literals, absolute_import
from django.db import models


class DateTimeModel(models.Model):
    """
    时间字段
    """
    ctime = models.DateTimeField('创建时间', auto_now_add=True)
    utime = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True
