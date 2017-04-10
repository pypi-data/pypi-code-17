#!/usr/bin/env python3

"""Grant class."""


from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String, Table,
                        Text)
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from ..db import db
from .Base import Base

grant_mappings = Table(
    'grants_mappings', Base.metadata,
    Column('_grant', ForeignKey('grants_dictionary.id', onupdate='CASCADE', ondelete='CASCADE'),
           primary_key=True),
    Column('_gives', ForeignKey('grants_dictionary.id', onupdate='CASCADE', ondelete='CASCADE'),
           primary_key=True)
)


class Grant(Base):

    """Grant class."""

    __tablename__ = 'grants_dictionary'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), index=True)
    description = Column(Text)
    internal = Column(Boolean, server_default='false')
    grants = relationship('Grant', secondary=grant_mappings,
                          primaryjoin=(id == grant_mappings.c._grant),
                          secondaryjoin=(id == grant_mappings.c._gives),
                          collection_class=attribute_mapped_collection('name'))
    _cache = {}

    granted_by = relationship('Grant', secondary=grant_mappings,
                              primaryjoin=(id == grant_mappings.c._gives),
                              secondaryjoin=(id == grant_mappings.c._grant),
                              collection_class=attribute_mapped_collection('name'))

    def allGrants(self):
        """return list of all grants given, recursively checked"""
        rq = (db.query(Grant).filter(Grant.id == self.id).cte(name='basegrant', recursive=True))
        q = (db.query(Grant)
             .select_entity_from(rq.union_all(
                 db.query(Grant)
                 .join(grant_mappings, grant_mappings.c._gives == Grant.id)
                 .join(rq, grant_mappings.c._grant == rq.c.id))))
        return q.all()

    @property
    def users(self):
        """Return all users having this grant either directly or indirectly"""
        from .User import user_grants, User

        rq = db.query(user_grants.c._user, user_grants.c._grant).cte(name='basegrant', recursive=True)

        uids = rq.union_all(db.query(rq.c._user, grant_mappings.c._gives)
                            .join(grant_mappings, grant_mappings.c._grant == rq.c._grant))

        return (db.query(User).join(uids, User.id == uids.c._user).filter(uids.c._grant == self.id)
                .order_by(User.login, User.id))

    @classmethod
    def get(cls, name):
        """Get grant by name.

        Caches grant ids so that next use tries to fetch it from
        SQLAlchemy cache. Caching Grant object directly is not feasible as
        it may survive longer than session in which it was fetched.
        """
        if name in cls._cache:
            grant = db.query(cls).get(cls._cache[name])
        elif str(name).isdecimal():
            grant = db.query(cls).get(name)
        else:
            grant = db.query(cls).filter_by(name=name).one()
            cls._cache[name] = grant.id

        return grant

    @classmethod
    def updateAll(cls):
        """Sync grants definitions from imported Python dictionaries"""

        grants = cls.systemGrants()
        dbgrants = {g.name: g for g in db.query(Grant).all()
                    if g.name.isupper()}
        for grant_name, grant_info in grants.items():
            if grant_name not in dbgrants:
                db.add(Grant(name=grant_name,
                             internal=grant_info.get('internal', False)))
            elif grant_info.get('internal', False) != dbgrants[grant_name].internal:
                dbgrants[grant_name].internal = grant_info.get('internal', False)
        db.commit()

    @classmethod
    def systemGrants(cls):
        """return dictionary of all system grants with their descriptions"""

        import pkgutil
        from importlib import import_module
        from .. import _grants

        result = {}

        for mdata in pkgutil.iter_modules(_grants.__path__):
            mod = import_module(_grants.__package__+'.'+mdata[1])  # pylint: disable=no-member
            result.update(getattr(mod, 'grants'))

        return result
