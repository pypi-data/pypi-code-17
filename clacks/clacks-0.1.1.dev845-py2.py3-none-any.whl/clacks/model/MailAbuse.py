#!/usr/bin/env python3

"""MailAbuse class."""

from sqlalchemy import Column, DateTime, Integer, cast, func
from sqlalchemy.dialects.postgresql import INET, INTERVAL

from ..db import db
from .Base import Base


class MailAbuse(Base):

    """MailAbuse class."""

    __tablename__ = 'mail_abuse'

    ip = Column(INET, primary_key=True)
    count = Column(Integer, server_default='1', nullable=False)
    last = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    @staticmethod
    def is_captcha_required(limit=1, increment=True, period=24):
        """checks whether given ip sent message too many times
           for a period given"""

        import cherrypy
        from random import random

        ip = cherrypy.request.remote.ip

        if ip == '127.0.0.2':  # it is set when there's no connection
            # happens sometimes, can't help it
            return True

        if random() > 0.99:
            db.query(MailAbuse)\
              .filter(MailAbuse.last < func.now() - cast('%d hour' % period, INTERVAL))\
              .delete(False)
            db.commit()

        row = db.query(MailAbuse).filter_by(ip=ip).first()

        if increment:
            if row:
                row.count += 1
            else:
                db.add(MailAbuse(ip=ip))
            db.commit()

        return row and row.count >= limit
