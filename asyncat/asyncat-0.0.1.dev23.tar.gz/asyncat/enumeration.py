#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This module provides enumeration used by this package."""
from __future__ import print_function, division, unicode_literals

from enum import Enum


class StatusState(Enum):
    """State of status"""
    pending = "pending"
    success = "success"
    error = "error"
    failure = "failure"


class Scope(Enum):
    """
    Scopes of user, more info see
    `here<https://developer.github.com/v3/oauth/#scopes>_`.
    """
    user = "user"
    user_email = "user:email"
    user_follow = "user:follow"
    public_repo = "public_repo"
    repo = "repo"
    repo_deployment = "repo_deployment"
    repo_status = "repo:status"
    delete_repo = "delete_repo"
    notifications = "notifications"
    gist = "gist"
    read_repo_hook = "read:repo_hook"
    write_repo_hook = "write:repo_hook"
    admin_repo_hook = "admin:repo_hook"
    admin_org_hook = "admin:org_hook"
    read_org = "read:org"
    write_org = "write:org"
    admin_org = "admin:org"
    read_public_key = "read:public_key"
    write_public_key = "write:public_key"
    admin_public_key = "admin:public_key"
    read_gpg_key = "read:gpg_key"
    write_gpg_key = "write:gpg_key"
    admin_gpg_key = "admin:gpg_key"
