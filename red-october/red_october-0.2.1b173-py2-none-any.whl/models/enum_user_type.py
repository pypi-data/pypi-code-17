# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from enum import Enum


class EnumUserType(Enum):
    """ It provides possible user encryption types for Red October.

    Attributes:
        rsa (int): Uses RSA encryption.
        ecc (int): Uses ECC encruyption.
    """
    rsa = 1
    ecc = 2
