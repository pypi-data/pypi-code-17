#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#
from .models import Credentials


def replyify_token_is_valid(user):
    try:
        return Credentials.objects.get(user=user).is_valid()
    except Credentials.DoesNotExist:
        return False
