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

"""Database model for Selenol account."""

from selenol_python.persistences import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import backref, object_session, relationship


class AccountUser(Base):
    """System user."""

    __tablename__ = 'account_user'

    id = Column(Integer, primary_key=True)

    name = Column(Text)

    email = Column(Text)

    @property
    def groups(self):
        """Return all the activated groups of the user.

        Because of the relation is not a direct relation but:
        AccountUser - NotificationRequest - AccountGroup, we need a way to be
        able to restore easily the groups of the user.
        """
        return object_session(self).query(
            AccountMembershipRequest).filter(
                AccountMembershipRequest.user_id == self.id).filter(
                    AccountMembershipRequest.replied_at.isnot(None)).join(
                        AccountGroup).with_entities(AccountGroup)


class AccountOAuthIdentity(Base):
    """OAuth identity."""

    __tablename__ = 'account_oauth_identity'

    id = Column(Integer, primary_key=True)

    service = Column(Text)

    user_identifier = Column(Text)

    access_token = Column(Text)

    created = Column(DateTime)

    user_id = Column(ForeignKey(AccountUser.id, use_alter=True))

    user = relationship(AccountUser,
                        backref=backref('oauth_identities', lazy='dynamic'))


class AccountSession(Base):
    """Token relation with users."""

    __tablename__ = 'account_session'

    id = Column(Integer, primary_key=True)

    user_id = Column(ForeignKey(AccountUser.id, use_alter=True))

    token = Column(Text)

    user = relationship(AccountUser,
                        backref=backref('sessions', lazy='dynamic'))


class AccountGroup(Base):
    """System group."""

    __tablename__ = 'account_group'

    id = Column(Integer, primary_key=True)

    name = Column(Text, unique=True)

    created = Column(DateTime)

    creator_id = Column(ForeignKey(AccountUser.id, use_alter=True))

    creator = relationship(AccountUser,
                           backref=backref('owned_groups', lazy='dynamic'))

    @property
    def users(self):
        """Return all the activated users of the group.

        Because of the relation is not a direct relation but:
        AccountUser - NotificationRequest - AccountGroup, we need a way to be
        able to restore easily the users of the group.
        """
        return object_session(self).query(
            AccountMembershipRequest).filter(
                AccountMembershipRequest.group_id == self.id).filter(
                    AccountMembershipRequest.replied_at.isnot(None)).join(
                        AccountUser).with_entities(AccountUser)


class AccountMembershipRequest(Base):
    """Membership request."""

    __tablename__ = 'account_membership_request'

    id = Column(Integer, primary_key=True)

    user_id = Column(ForeignKey(AccountUser.id, use_alter=True))

    group_id = Column(ForeignKey(AccountGroup.id, use_alter=True))

    requested_at = Column(DateTime)

    replied_at = Column(DateTime, nullable=True)

    user = relationship(AccountUser,
                        backref=backref('membership_requests', lazy='dynamic'))

    group = relationship(AccountGroup,
                         backref=backref('membership_requests',
                                         lazy='dynamic'))


class AccountNotification(Base):
    """User notification."""

    __tablename__ = 'account_notification'

    id = Column(Integer, primary_key=True)

    user_id = Column(ForeignKey(AccountUser.id, use_alter=True))

    content = Column(Text)

    created_at = Column(DateTime)

    saw_at = Column(DateTime, nullable=True)

    user = relationship(AccountUser,
                        backref=backref('notifications', lazy='dynamic'))
