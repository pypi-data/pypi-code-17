# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from enum import Enum


class EnumUserRole(Enum):
    """ It provides possible user roles for Red October.

    Attributes:
        delete (int): User is deleted or scheduled to be so.
        revoke (int): Normal user, revoke administrative rights.
        admin (int): User has administrative rights.
        user (int): Alias for `revoke`.
    """
    delete = 1
    revoke = 2
    admin = 3
    user = revoke
