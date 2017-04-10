#!/usr/bin/env python3

"""User class."""

# pylint: disable=no-member,attribute-defined-outside-init

import crypt

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Table, func, select)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, column_property, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from ..db import db
from .Base import Base
from .Grant import Grant

user_grants = Table(
    'users_grants', Base.metadata,
    Column('_user',
           ForeignKey('clients.id', onupdate='CASCADE', ondelete='CASCADE'),
           primary_key=True),
    Column('_grant',
           ForeignKey('grants_dictionary.id', onupdate='CASCADE', ondelete='CASCADE'),
           primary_key=True)
)

class User(Base):
    """User class."""

    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    email = Column(String(256))
    _password = Column('password', String(256))
    name = Column(String(256))
    surname = Column(String(256))
    active = Column('_active', Boolean, server_default='false')
    activationCode = Column('_activation_code', String(128))
    created = Column(DateTime, server_default=func.now())
    phone = Column('phone_number', String(32))
    newsletter = Column(Boolean, server_default='false')
    vatid = Column('nip', String(32))
    login = Column(String(256), nullable=False, unique=True)
    fax = Column('fax_number', String(128))
    company = Column(String(256))
    cellphone = Column('cellphone_number', String(32))
    # obsolete, kept for PHP compat only:
    __orders = Column('orders', Integer, server_default='0', nullable=False)
    wantsVatInvoice = Column('fvat', Boolean, server_default='false')
    facebookUID = Column('facebook_uid', String)
    facebookToken = Column('facebook_token', String)
    role = Column(String, server_default='client')
    _parent = Column(ForeignKey('clients.id', onupdate='CASCADE', ondelete='CASCADE', deferrable=True),
                     index=True)

    parent = relationship('User',
                          backref=backref("dependants", lazy="dynamic"),
                          remote_side=[id])

    _grants_given = relationship('Grant', secondary=user_grants,
                                 collection_class=attribute_mapped_collection('name'))

    @hybrid_property
    def allDependantsAndMe(self):
        """Return not only direct dependants but full list with nested ones as well."""
        rq = db.query(User).filter_by(id=self.id).cte(name='baseuser', recursive=True)
        q = db.query(User).select_entity_from(rq.union_all(
            db.query(User).filter(User._parent == rq.c.id)))
        return q

    @hybrid_property
    def allDependants(self):
        """Returns flattened list of all dependant users."""
        return self.allDependantsAndMe.filter(User.id != self.id)

    @property
    def grants(self):
        """Return full list of grants both direct and indirect."""
        if not hasattr(self, '_grants') or self._grants is None:
            from .Grant import grant_mappings
            rq = (db.query(Grant).join(user_grants).join(User)
                  .filter(User.id == self.id).cte(name='basegrant', recursive=True))
            q = (db.query(Grant)
                 .select_entity_from(rq.union_all(
                     db.query(Grant)
                     .join(grant_mappings, grant_mappings.c._gives == Grant.id)
                     .join(rq, grant_mappings.c._grant == rq.c.id))))
            self._grants = frozenset((g.name for g in q.all()))
        return self._grants

    def setGrant(self, grant):
        """Set grant, both Grant instance and grant name are accepted."""
        if not isinstance(grant, Grant):
            grant = db.query(Grant).filter_by(name=grant).one()
        self._grants_given[grant.name] = grant
        self._grants = None
        db.flush()

    def dropGrant(self, grant):
        """Remove direct grant from user.

        Can't remove indirect grant. User all grants list is refreshed.
        """
        if isinstance(grant, Grant):
            grant = grant.name
        try:
            self._grants_given.pop(grant)
        except KeyError:
            pass
        else:
            self._grants = None
            db.flush()

    def isDirectGrant(self, grant):
        """Checks whether given grant is direct one."""
        if isinstance(grant, Grant):
            grant = grant.name
        return grant in self._grants_given

    def granted(self, grant, admin=True):
        """Check if user has given grant."""
        return self.grantedAny((grant,), admin)

    def grantedAny(self, grants, admin=True):
        """Check if user has any of given grants."""
        return (admin and 'SITE_ADMIN' in self.grants) or any(
            (g.name if isinstance(g, Grant) else g) in self.grants for g in grants
        )

    def grantedAll(self, grants):
        """Check if user has all of given grants."""
        return 'SITE_ADMIN' in self.grants or all(g in self.grants for g in grants)

    @hybrid_property
    def password(self):
        """password getter"""
        return self._password

    @password.setter
    def password(self, newpass):
        """password setter"""
        if newpass.startswith('$6$'):
            self._password = newpass
        else:
            self._password = crypt.crypt(newpass, crypt.METHOD_SHA512)

    def checkPassword(self, password):
        """Validate password against stored one."""
        if self.password[:1] != '$':
            return False
        return crypt.crypt(password, self.password) == self.password

    def isParentOf(self, user):
        """Check if given user is parent of given one.

        Warning: this method is not cycle resistant"""

        return user.isChildOf(self)

    def isChildOf(self, user):
        """Check if given user is child of given one"""
        if self.parent == user:
            return True
        elif self.parent:
            return self.parent.isChildOf(user)
        else:
            return False

    def fullName(self):
        """Get full name"""
        return ' '.join((self.name, self.surname))

    def export(self):
        """Return JSON friendly dictionary of object's state"""

        result = {attr: getattr(self, attr) for attr in
                  ['id', 'email', 'name', 'surname', 'active', 'activationCode',
                   'created', 'phone', 'newsletter', 'vatid', 'login', 'fax',
                   'company', 'cellphone', 'wantsVatInvoice',
                   'facebookUID', 'role', '_parent']}

        result['created'] = str(result['created'])[:19]

        result['addresses'] = [a.export() for a in self.addresses]

        if hasattr(self, 'wallets'):
            for wallet in self.wallets:
                result.update(wallet.export())
        return result


_cntable = User.__table__.alias()

User.dependantsCount = column_property(
    select([func.count(_cntable.c._parent)],
           _cntable.c._parent == User.id).correlate(User.__table__),
    deferred=True)
