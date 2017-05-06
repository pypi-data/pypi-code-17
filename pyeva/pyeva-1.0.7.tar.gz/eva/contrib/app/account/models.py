# coding: utf-8

'''附件
'''

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

from app.oss.models import OSSUserObject


class AccountAvatar(UIDMixin, ORMBase):
    '''用户图像

    用户可以保存多个头像
    '''

    __tablename__ = 'account_avatar'

    id = Column(Integer, Sequence('account_avatar_id_seq'), primary_key=True)

    user_id = Column(Integer, ForeignKey('auth_user.id'))
    user = relationship("User", backref="avatars")

    avatar_id = Column(Integer, ForeignKey('oss_user_object.id'))
    avatar = relationship("OSSUserObject")

    is_primary = Column(Boolean, default=False)

    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, user, avatar, is_primary=False):
        self.user_id = user.id
        self.avatar_id = avatar.id
        self.is_primary = is_primary
