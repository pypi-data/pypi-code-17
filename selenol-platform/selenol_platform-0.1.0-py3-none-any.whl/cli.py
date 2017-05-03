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

"""Application module to manage the services."""

import click
import pkg_resources

from selenol_python.persistences import Base, get_engine, session_creator

from .pool import SelenolPool


def load_service_entrypoints(group):
    """Apply the given function to all the service entripoints."""
    return [item.load() for item in
            pkg_resources.iter_entry_points(group=group)]


@click.group()
def cli_group():
    """CLI tool."""


@cli_group.group(name='db')
def db_group():
    """DB related methods."""


@cli_group.group(name='fixtures')
def fixtures_group():
    """Fixture related methods."""


@fixtures_group.command('create')
@click.option('-c', '--connection', default=None)
def create_fixtures(connection):
    """Create all the fixtures used by the application."""
    session = session_creator(connection)

    for fixture in load_service_entrypoints('selenol.fixtures'):
        fixture(session)


@db_group.command(name='create')
@click.option('-c', '--connection', default=None)
def create_db(connection):
    """Create all the database base."""
    engine = get_engine(connection)

    load_service_entrypoints('selenol.services')

    Base.metadata.create_all(engine)


@cli_group.command()
def run():
    """Run the service."""
    services = load_service_entrypoints('selenol.services')
    pool = SelenolPool(services)
    pool.serve()
