from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy_utils import database_exists, create_database, drop_database
from contextlib import contextmanager
import pytest
from . import settings

DeclarativeBase = declarative_base()

def db_connect(database):
    return create_engine(URL(**database))

def db_create(engine):
    if not database_exists(engine.url):
        create_database(engine.url)
        DeclarativeBase.metadata.create_all(engine)

def db_drop(engine):
    if database_exists(engine.url):
        drop_database(engine.url)

def session_connect(db_connect):
    return sessionmaker(bind=db_connect)

Session = session_connect(db_connect(settings.DATABASE))

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

@contextmanager
def session_scope_refresh():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()	
        raise
    finally:
        session.close()

