# coding: utf-8

'''附件
'''

import os
import datetime
import logging

from sqlalchemy import (
    Table,
    Column,
    Integer,
    Float,
    String,
    Boolean,
    Sequence,
    DateTime,
    Text,
    ForeignKey
)
from sqlalchemy.orm import backref, relationship

from eva.db.models import UIDMixin
from eva.orm import ORMBase
from eva.conf import settings


class OSSObject(UIDMixin, ORMBase):
    '''存储对象
    '''

    __tablename__ = 'oss_object'

    id = Column(Integer, Sequence('oss_object_id_seq'), primary_key=True)

    size = Column(Integer)
    checksum = Column(String(128))

    created = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, size, checksum):
        self.size = size
        self.checksum = checksum


class OSSUserObject(UIDMixin, ORMBase):
    '''用户的OSS

    将用户与 Object 关联（可以消冗）
    '''

    __tablename__ = 'oss_user_object'

    id = Column(Integer, Sequence('oss_user_object_id_seq'), primary_key=True)

    user_id = Column(Integer, ForeignKey('auth_user.id'))
    user = relationship("User")

    obj_id = Column(Integer, ForeignKey('oss_object.id'))
    obj = relationship("OSSObject")

    # 文件名便于 nginx 静态下载, 用户追溯
    filename = Column(String(256))

    name = Column(String(256))
    summary = Column(Text)

    # 是否公开分享
    is_public = Column(Boolean, default=True)

    # Used by admin
    is_locked = Column(Boolean, default=False)

    # TODO: 增加下载、引用、标签、评论等属性

    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, user, obj, filename, name=None, summary=None):
        self.user_id = user.id
        self.obj_id = obj.id
        self.filename = filename
        if name:
            self.name = name
        if summary:
            self.summary = summary

    @property
    def static_url(self):
        # TODO: 为每个用户单独做个软连接，以便直接使用 nginx 下载
        return os.path.join(settings.OSS_STATIC_URL_PREFIX,
                            "{0}/{1}_{2}".format(self.user.uid, self.obj.checksum, self.filename))
