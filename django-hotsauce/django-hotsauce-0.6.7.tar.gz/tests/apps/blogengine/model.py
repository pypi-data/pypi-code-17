#!/usr/bin/env python
# Copyright (C) 2007-2012 Etienne Robillard <erob@gthcfoundation.org>
# All rights reserved.
# -*- coding: utf-8 -*-
# <LICENSE=ISC>
# Default model classes for use in BlogEngine

from notmm.dbapi.orm import model, ClientStorageProxy
from notmm.utils.django_settings import LazySettings

_settings = LazySettings()

class Author(model.Model):
    class Meta:
        db_backend = ClientStorageProxy
        db_addr = '127.0.0.1:4343'

class Comment(model.Model):
    class Meta:
        db_backend = ClientStorageProxy
        db_addr = '127.0.0.1:4343'

class Message(model.Model):
    class Meta:
        db_backend = ClientStorageProxy
        db_addr = '127.0.0.1:4343'

# Generic voting Manager objects
#class PollManager(object):
#    objects = RelationProxy(db.Poll)
MessageManager = model.ModelManager(Message)

