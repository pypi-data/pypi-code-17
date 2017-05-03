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

"""Model serializers."""

import json


def group_serializer(group):
    """Group information serializer."""
    return {
        'group_id': group.id,
        'name': group.name,
        'created': str(group.created),
        'creator': {
            'user_id': group.creator_id,
            'name': group.creator.name
        },
        'members': {
            member.id: {
                'name': member.name
            } for member in group.users}
    }


def group_membership_request_serializer(membership_request):
    """Membership request information serializer."""
    return {
        'membership_request_id': membership_request.id,
        'user': {
            'user_id': membership_request.user_id,
            'name': membership_request.user.name
        },
        'requested_at': str(membership_request.requested_at),
        'group': {
            'group_id': membership_request.group_id,
            'name': membership_request.group.name
        }
    }


def user_serializer(user):
    """User information serializer."""
    return {
        'user_id': user.id,
        'name': user.name,
        'email': user.email
    }


def user_groups_serializer(user):
    """User group serializer."""
    return {
        'member': [group_serializer(group) for group in user.groups],
        'owner': [group_serializer(group) for group in user.owned_groups],
    }


def oauth_info_serializer(oauth):
    """Oauth information serializer."""
    return {
        'name': oauth['name'],
        'request_url': oauth['request_url'],
    }


def login_serializer(login, token=None):
    """Login information serializer."""
    return {
        'user_id': login.id,
        'name': login.name,
        'email': login.email,
        'token': token,
        'oauth': [{
            'service': identity.service,
            'access_token': identity.access_token,
            'created': str(identity.created)
        } for identity in login.oauth_identities]
    }


def notification_serializer(notification):
    """Notification serializer."""
    return {
        'notification_id': notification.id,
        'created_at': str(notification.created_at),
        'content': json.loads(notification.content),
    }
