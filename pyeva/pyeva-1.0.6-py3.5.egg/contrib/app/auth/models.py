# coding: utf-8

import os
import time
import datetime
import logging

from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table, Column, ForeignKey, Sequence
from sqlalchemy import Integer, String, Boolean, DateTime, Text

from eva.orm import ORMBase
from eva.utils.auth import enc_login_passwd, check_login_passwd
from eva.utils.time_ import (
    after_seconds,
    rfc3339_string
)
from eva.utils.random_ import random_ascii, random_digit
from eva.models.uuid import UUIDMixin
from eva.conf import settings
from eva.utils.translation import ugettext_lazy as _

from . import settings as auth_settings


GENDER_CHOICES = (
    ("male", _("Male")),
    ("female", _("Female")),
    ("secret", _("Secret")),
)

user_groups = Table(
    'auth_user__group', ORMBase.metadata,
    Column('user_id', Integer, ForeignKey('auth_user.id')),
    Column('group_id', Integer, ForeignKey('auth_group.id'))
)


group_permissions = Table(
    'auth_group__permission', ORMBase.metadata,
    Column('group_id', Integer, ForeignKey('auth_group.id')),
    Column('permission_id', Integer, ForeignKey('auth_permission.id')),
)


class Group(ORMBase):

    __tablename__ = 'auth_group'

    id = Column(Integer, Sequence('auth_group_id_seq'), primary_key=True)
    name = Column(String(30))
    description = Column(Text())

    def __init__(self, name, description=None):
        self.name = name
        if description:
            self.description = description


class User(ORMBase):

    __tablename__ = 'auth_user'

    id = Column(Integer, Sequence('auth_user_id_seq'), primary_key=True)

    uid = Column(Integer, unique=True, doc=_('User ID'))
    username = Column(String(32), unique=True, doc=_('Username'))
    password = Column(String(512), doc=_('Password'))
    email = Column(String(30), unique=True, doc=_('Email'))

    first_name = Column(String(30), doc=_('First Name'))
    last_name = Column(String(30), doc=_('Last Name'))
    nickname = Column(String(30), doc=_('Nickname'))
    gender = Column(Integer, doc=_('Gender'))

    is_active = Column(Boolean, default=True, doc=_('User is active'))
    is_staff = Column(Boolean, default=False, doc=_('User is staff'))
    is_superuser = Column(Boolean, default=False, doc=_('This is super user'))
    is_locked = Column(Boolean, default=False, doc=_('User has beed locked'))

    language = Column(String(12), default='zh-cn',
                      doc=_('The locale language'))

    last_active = Column(DateTime())
    last_login = Column(DateTime())
    date_joined = Column(DateTime(), default=datetime.datetime.utcnow)

    groups = relationship('Group', secondary=user_groups, backref='users')

    def __init__(self, uid, password, email=None):
        self.uid = uid
        self.password = enc_login_passwd(password)
        self.email = email

    @property
    def fullname(self):
        if self.language == 'zh-cn':
            return '{}{}'.format(self.last_name, self.first_name)
        else:
            return '{} {}'.format(self.first_name, self.last_name)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        return check_login_passwd(raw_password, self.password)

    def enc_password(self, raw_password):
        return enc_login_passwd(raw_password)

    def set_password(self, raw_password):
        self.password = enc_login_passwd(raw_password)

    @property
    def ibase(self):
        # TODO: showname
        return {
            'id': self.uid,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'nickname': self.nickname if self.nickname else self.username,
            'email': self.email,
            'gender': self.gender,
            'is_staff': self.is_staff,
            'is_superuser': self.is_superuser,
            'is_locked': self.is_locked,
            'language': self.language,
            'last_active': rfc3339_string(self.last_active),
            'last_login': rfc3339_string(self.last_login),
            'date_joined': rfc3339_string(self.date_joined),
        }

    @property
    def iowner(self):
        return self.ibase

    @property
    def iadmin(self):
        return self.ibase

    @property
    def isimple(self):
        return {
            "id": self.uid,
            "username": self.username,
            "nickname": self.nickname
        }


class Permission(ORMBase):

    __tablename__ = 'auth_permission'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    codename = Column(String(100), unique=True)

    groups = relationship("Group", secondary=group_permissions,
                          backref="permissions")

    def __init__(self, name, codename):
        self.name = name
        self.codename = codename


class Session(ORMBase):

    __tablename__ = 'auth_session'

    id = Column(Integer, Sequence('auth_session_id_seq'), primary_key=True)
    sid = Column(String(128), unique=True)

    user_id = Column(Integer, ForeignKey('auth_user.id'))
    user = relationship("User", backref='sessions')

    from_ip = Column(String(64))  # 当前会话的来源IP, 可增强安全

    expired = Column(DateTime())

    def __init__(self, sid, user, from_ip=None):
        self.sid = sid
        self.user_id = user.id
        self.expired = after_seconds(settings.SESSION_COOKIE_AGE)
        if from_ip:
            self.from_ip = from_ip

    def refresh_expired(self):
        '''重新激活失效时间'''
        self.expired = after_seconds(settings.SESSION_COOKIE_AGE)

    def is_valid(self):
        return datetime.datetime.utcnow() < self.expired


class AuthIdentifier(UUIDMixin, ORMBase):
    """验证码"""

    __tablename__ = 'auth_identifier'

    id = Column(Integer, Sequence('auth_identifier_id_seq'), primary_key=True)

    uuid = Column(String(36), nullable=False, unique=True)
    type = Column(String(16))    # 验证码类型, 为何种验证?
    code = Column(String(6))     # 验证码
    data = Column(String(128))   # 数据
    expired = Column(DateTime())

    def __init__(self, type):
        self.type = type
        self.expired = after_seconds(auth_settings.AUTH_IDENTIFIER_TIMEOUT)

    def is_valid(self):
        return datetime.datetime.utcnow() < self.expired


def create_session(db, user, from_ip=None):
    '''创建新的会话凭证
    '''
    # 得到新 sid
    while True:
        sid = random_ascii(128)
        c = db.query(Session).filter_by(sid=sid).count()
        if not c:
            break

    # TODO: 删除旧的 session

    session = Session(sid, user, from_ip=from_ip)
    db.add(session)
    db.commit()

    return session


def clear_session(db, user, from_ip=None):
    '''清除 User 会话凭证
    '''
    for s in self.db.query(Session).filter_by(user_id=user.id):
        db.delete(s)
    db.commit()


def create_user(db, password, email, **kwargs):

    exist_user = db.query(User.id).filter_by(email=email).first()
    if exist_user:
        logging.warn(
            "can not create user: email address (%s) was existed", email)
        return

    import random
    getuid = False
    # TODO: best uid
    start = 10000
    while not getuid:
        max_try = 100
        i = 0
        end = start + 10000
        while i < max_try:
            i += 1
            uid = random.randint(start, end)
            if not db.query(User).filter_by(uid=uid).first():
                getuid = True
                break
        # be safe!
        if start > 1000000:
            break
        start += 10000

    if not getuid:
        logging.error("find available uid failed!")
        return

    user = User(uid, password, email)
    user.first_name = kwargs.get("first_name", "")
    user.last_name = kwargs.get("last_name", "")
    user.nickname = kwargs.get("nickname", "")
    user.username = kwargs.get("username", email)  # TODO: fix me!

    db.add(user)
    db.commit()

    logging.info("create user (username=%s, uid=%s, email=%s) success",
                 user.username, user.uid, user.email)

    return user


def create_identifier(db, type, data=None):
    c = AuthIdentifier(type)
    c.uuid = AuthIdentifier.gen_uuid(db)
    c.code = random_digit(6)
    if data:
        c.data = data
    db.add(c)
    db.commit()
    return c
