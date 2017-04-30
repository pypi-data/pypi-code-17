#! coding=utf-8
"""DigitalOcean APIv2 user module"""
__author__ = "Sriram Velamur <sriram.velamur@gmail.com>"
__all__ = ("DOUser",)

import sys
sys.dont_write_bytecode = True

from .base import BaseObject


class DOUser(BaseObject):

    """DigitalOcean user object"""

    email_verified, droplet_count, \
        droplet_limit, uuid, email = (None,) * 5

    def __repr__(self):
        return "DigitalOcean User: {0} [{1}]".format(
            self.uuid, self.email)

    def __str__(self):
        return "DigitalOcean User: {0} [{1}]".format(
            self.uuid, self.email)
