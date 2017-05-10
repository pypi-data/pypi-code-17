#!/usr/bin/env python
#-*-coding:utf-8-*- 

import datetime
import os
import time 

import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String,Text,DateTime,Date,Float,Boolean,ForeignKey,Index,BLOB
from sqlalchemy import func

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship,backref

from sqlalchemy.ext.declarative import declarative_base

#from sqlalchemy.schema import DefaultClause

From_RDBS_DATABASE_URL = 'mysql://root:root@192.168.20.40/fits?charset=utf8'

from_engine = create_engine(From_RDBS_DATABASE_URL)
from_Session = sessionmaker(bind=from_engine)
from_session = from_Session()
from_Base = declarative_base()

To_RDBS_DATABASE_URL = 'mysql://qiulimao:mimashiroot@10.0.0.100/pages?charset=utf8'
to_engine = create_engine(To_RDBS_DATABASE_URL)
to_Session = sessionmaker(bind=to_engine)
to_session = to_Session()
to_Base = declarative_base()

class RawWebContent(from_Base):
    """
    """
    __tablename__ = "source_ifeng"
    
    id = Column(Integer,primary_key=True)
    title = Column(String(128))
    content_html = Column(Text)
    html = Column(Text)    
    url = Column(String(512))

    def __repr__(self):
        represent = "<WebContent %s>" % self.title
        return represent




class WebContent(to_Base):
    """
    """
    __tablename__ = "webpage"
    
    id = Column(Integer,primary_key=True)
    title = Column(String(128))
    html = Column(Text)
    content = Column(Text)
    noise = Column(Text)    
    url = Column(String(512))

    def __repr__(self):
        represent = "<WebContent %s>" % self.title
        return represent

if __name__ == "__main__":
    """
    """
    to_Base.metadata.create_all(to_engine)