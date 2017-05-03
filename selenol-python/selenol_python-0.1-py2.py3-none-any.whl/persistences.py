# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Selenol persistences implementation."""

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def session_creator(connection=None):
    """Database session creator.

    :param connection: Database string connection.
    """
    engine = get_engine(connection)
    return sessionmaker(bind=engine)()


def get_engine(connection=None):
    """Return the database engine.

    :param connection: Database string connection.
    """
    return create_engine(connection or
                         os.environ.get('DATABASE', 'sqlite:///database.db'))
