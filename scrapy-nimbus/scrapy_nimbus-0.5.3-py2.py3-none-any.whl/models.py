# -*- coding: utf-8 -*-
from __future__ import absolute_import
"""
Package Description
"""
import os
import sys
import logging
import json
from functools import wraps
from sqlalchemy.ext.declarative import ConcreteBase, AbstractConcreteBase, DeferredReflection
from sqlalchemy.ext.declarative.api import declared_attr
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy import MetaData
from sqlalchemy import text
from sqlalchemy import func
from sqlalchemy.orm import load_only

from .data import Base

__all__ = ["Base", "BaseModel", "create_table", ]


class BaseModel(AbstractConcreteBase, Base):
    pass


def create_table(engine, model):
    if model and engine and isinstance(model, Base):
        model.metadata.create_all(bind=engine)
    return True

#
# class ExampleModel(BaseModel):
#     __tablename__ = 'examples'
#     id = Column(Integer, primary_key=True, autoincrement=True, doc=u"ID")
#     link = Column(String(255), doc=u"原文链接", unique=True)
#     channel = Column(String(100), doc=u"频道", index=True)
#     tag = Column(String(100), doc=u"标签", index=True)
#     time = Column(String(30), doc=u"文章时间", index=True)
#     title = Column(String(255), doc=u"文章标题")
#     img = Column(String(255), doc=u"标题图片")
#     content = Column(Text(), doc=u"文章正文")
#     summary = Column(Text(), doc=u"文章摘要")
#     writer = Column(String(100), doc=u"作者")
#     number = Column(Integer, server_default='0', doc=u"阅读数量")
#     create_date = Column(DateTime, server_default=func.now(), doc=u"创建时间")
#     create_user = Column(String(36), doc=u"创建用户")
#     modify_date = Column(DateTime, server_onupdate=func.now(), doc=u"修改时间")
#     modify_user = Column(String(36), doc=u"修改用户")
#
#     def __init__(self, **kwargs):
#         self.section_id = kwargs.get("section_id", "")
#         self.title = kwargs.get("title", "")
#         self.img = kwargs.get("img", "")
#         self.content = kwargs.get("content", "")
#         self.summary = kwargs.get("summary", "")
#         self.writer = kwargs.get("writer", "")
#         self.link = kwargs.get("link", "")
#         self.time = kwargs.get("time", "")
#         self.channel = kwargs.get("channel", "")
#         self.tag = kwargs.get("tag", "")
#         # self.create_date = kwargs.get("create_date", "")
#         self.create_user = kwargs.get("create_user", u"爬虫")
#         # self.modify_date = kwargs.get("modify_date", "")
#         # self.modify_user = kwargs.get("modify_user", "")
