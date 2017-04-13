#!/usr/bin/env python
from notmm.dbapi.orm import model, ClientStorageProxy

class Message(model.Model):
    class Meta:
        db_backend = ClientStorageProxy
        db_addr = '127.0.0.1:4343'
