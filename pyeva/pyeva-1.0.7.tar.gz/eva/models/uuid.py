# coding: UTF-8

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.ext.declarative import declared_attr

from eva.utils.random_ import gen_uuid

#class UserMixin(object):
#
#    @declared_attr
#    def user_id(cls):
#        return Column(Integer, ForeignKey('auth_user.id'))


class UUIDMixin(object):

    #@declared_attr
    #def uuid(cls):
    #    return Column( String(36), nullable=False, unique = True )

    @classmethod
    def gen_uuid(cls, db):
        while True:
            x = gen_uuid()
            if not db.query(cls.uuid).filter_by(uuid=x).count():
                break
        return x
