# coding: UTF-8

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.ext.declarative import declared_attr

from eva.utils.translation import ugettext_lazy as _
from eva.utils.random_ import random_ascii


class UIDMixin(object):
    '''Unique Identifier

    初始范围使用:
    (26字母+10数字) ** 8位 = 2821109907456

    思考：
    1. 隐藏真实对象ID（避免猜测）
    2. 长度不宜太长
    '''

    @declared_attr
    def uid(cls):
        return Column(String(8), nullable=False, unique=True, doc=_("Unique Identifier"))

    @classmethod
    def gen_uid(cls, db):
        while True:
            x = random_ascii(8, ignorecase=True)
            if not db.query(cls.uid).filter_by(uid=x).count():
                break
        return x
