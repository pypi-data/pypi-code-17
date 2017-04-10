#!/usr/bin/env python3

""" Setting class """

from sqlalchemy import Column, Integer, String, text

from .Base import Base


class Setting(Base):

    """ Setting class """

    __tablename__ = 'settings'

    id = Column('setting_id', Integer, primary_key=True)
    name = Column(String(32), unique=True)
    description = Column(String(128))
    value = Column(String)
    type = Column(String(16))
    priority = Column(Integer, server_default=text("currval('settings_setting_id_seq'::regclass)"))
