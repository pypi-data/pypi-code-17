# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- PG specific tests
# :Created:   sab 24 ott 2015 12:52:33 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: Copyright (C) 2015, 2016, 2017 Lele Gaifax
#

from __future__ import absolute_import

import datetime, uuid

import pytest

from psycopg2.extras import DateRange

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sapg
from sqlalchemy.ext.declarative import declarative_base

from metapensiero.sqlalchemy.proxy.core import ProxiedQuery
from metapensiero.sqlalchemy.proxy.orm import ProxiedEntity
from metapensiero.sqlalchemy.proxy.filters import extract_filters


# Note: the echoed statements will be visible with "py.test -s"
engine = sa.create_engine('postgresql://localhost/mp_sa_proxy_test', echo=True)
Session = sa.orm.sessionmaker(bind=engine)


metadata = sa.MetaData(bind=engine)
Base = declarative_base(metadata=metadata)


class GUID(sa.TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses CHAR(32), storing as stringified hex value.
    """

    impl = sa.types.CHAR

    def load_dialect_impl(self, dialect, _PGUUID=sapg.UUID, _CHAR=sa.types.CHAR):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(_PGUUID())
        else:
            return dialect.type_descriptor(_CHAR(32))

    # NOTE: UUIDs are enforced *only* on PostgresQL, because doing that on MySQL right now
    #       would mean spending a lot of time fixing the assumptions that legacy code base
    #       is full of.

    def process_bind_param(self, value, dialect,
                           _UUID=uuid.UUID, _uuid3=uuid.uuid3, _ns=uuid.NAMESPACE_OID):
        if value is None:
            return value
        else:
            if isinstance(value, _UUID):
                return value.hex
            elif dialect.name == 'postgresql':
                try:
                    return _UUID(value).hex
                except (ValueError, AttributeError):
                    if not isinstance(value, str):
                        value = str(value)
                    return _uuid3(_ns, value).hex
            else:
                return value

    def process_result_value(self, value, dialect, _UUID=uuid.UUID):
        return value if value is None or dialect.name != 'postgresql' else _UUID(value)


class Product(Base):
    __tablename__ = 'products'

    id = sa.Column(GUID, primary_key=True,
                   info=dict(label='id', hint='the product id'))
    brand = sa.Column(sa.String(64),
                      info=dict(label='brand', hint='the product brand'))
    description = sa.Column(sapg.HSTORE,
                            info=dict(label='description', hint='the product description'))
    availability = sa.Column(sapg.DATERANGE,
                             info=dict(label='availability', hint='period of availability'))


def setup():
    metadata.create_all()

    session = Session()

    p = Product(id='frizione', brand='Allga San®',
                description={'it': 'Frizione', 'de': 'Einreibung'})
    session.add(p)

    p = Product(id='orologio', brand='Breitling',
                description={'it': 'Orologio', 'en': 'Watch'})
    session.add(p)

    p = Product(id='fragole', brand='Km0',
                description={'it': 'Fragole', 'en': 'Strawberries'},
                availability=DateRange(datetime.date(2017, 3, 23),
                                       datetime.date(2017, 4, 24)))
    session.add(p)

    session.commit()


def teardown():
    metadata.drop_all()


@pytest.mark.parametrize('column,args,expected_snippet', [
    ( Product.__table__.c.description['it'],
      dict(filter_col='description', filter_value='~=bar'),
      ' LIKE ' ),
    ( Product.__table__.c.availability,
      dict(filter=[dict(property='availability', value=datetime.date(2017, 4, 1))]),
      ' @> '),
])
def test_operators(column, args, expected_snippet):
    conds = extract_filters(args)
    assert len(conds) == 1
    cond = conds[0]
    filter = cond.operator.filter(column, cond.value)
    assert expected_snippet in str(filter)


def test_filters():
    proxy = ProxiedEntity(Product)

    sas = Session()

    res = proxy(sas, filters=[dict(property='availability',
                                   value=datetime.date(2017, 4, 1))])
    assert res[0].description['it'] == 'Fragole'
    sas.commit()


def test_sort_1():
    proxy = ProxiedEntity(Product)

    sas = Session()
    res = proxy(sas)
    sas.commit()

    assert res


def test_sort_2():
    t = Product.__table__

    proxy = ProxiedQuery(sa.select([t.c.id, t.c.description['it']]))

    sas = Session()

    res = proxy(sas, sort_col='description')
    sas.commit()

    assert res[0][1] < res[1][1]

    res = proxy(sas, sort_col='description', sort_dir='DESC')
    sas.commit()

    assert res[0][1] > res[1][1]
