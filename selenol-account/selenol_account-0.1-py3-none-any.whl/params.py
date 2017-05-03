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

"""Params declarations."""

from selenol_python.params import get_object_from_session

from selenol_account.models import AccountUser


def get_user_from_session():
    """."""
    def function_wrapper(service, message):
        """."""
        return get_object_from_session(
            AccountUser, ['user_id'])(service, message)
    return function_wrapper
