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

"""Fixtures."""

from datetime import datetime

from .models import AccountGroup, AccountUser


def create_admin_user_public_group(session):
    """Create the admin user and the public group.

    :param session: Database session.
    """
    admin_user = AccountUser(name="admin", email="admin@admin.com")
    session.add(admin_user)
    session.commit()

    public_group = AccountGroup(name="public", creator_id=admin_user.id,
                                created=datetime.now())
    session.add(public_group)
    session.commit()
