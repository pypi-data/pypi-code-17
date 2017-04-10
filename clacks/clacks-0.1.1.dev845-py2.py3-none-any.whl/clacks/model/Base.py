#!/usr/bin/env python3

"""Definition of class Base."""

from sqlalchemy.ext.declarative import declarative_base

from ..db import db

__all__ = ['Base']


class RepresentableBase(object):
    """ Helper class for SQLAlchemy model Base to provide unified default __repr__()"""

    def __repr__(self):
        return repr({key: val for key, val in self.__dict__.items()
                     if key != '_sa_instance_state'})


Base = declarative_base(metadata=db.meta, cls=RepresentableBase)  # pylint: disable=C0103
