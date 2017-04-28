# -*- coding: utf-8 -*-
import sys

from .. import contstants
from ..models import Log
from ..utils import verify_user, verify_exception


def create_by_exception(exception, message, location, user=None, tag=None, code_error=None,
                        level=contstants.LEVEL_ERROR, status=contstants.STATUS_ACTIVE):
    user = verify_user(user)
    exception_name = verify_exception(exception)
    log = Log(
        title=exception_name,
        message=message,
        code_error=code_error,
        location=location,
        user=user,
        level=level,
        tag=tag,
        status=status
    )
    log.save()
    return log


def create_log(title, message, location=None, user=None, tag=None, code_error=None,
               level=contstants.LEVEL_INFO, status=contstants.STATUS_ACTIVE):
    user = verify_user(user)

    log = Log(
        title=title,
        message=message,
        code_error=code_error,
        location=location,
        user=user,
        level=level,
        tag=tag,
        status=status
    )
    log.save()
    return log