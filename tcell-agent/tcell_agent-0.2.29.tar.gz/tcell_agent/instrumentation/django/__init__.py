# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

from __future__ import unicode_literals

import logging

from tcell_agent.agent import TCellAgent

_started = False
_route_table_sent = False
_dlp_success = False
_default_charset = 'utf-8'

LOGGER = logging.getLogger('tcell_agent').getChild(__name__)


def _instrument():
    from tcell_agent.instrumentation.django.middleware.csrf_exception_middleware import instrument_csrf_view_middleware
    from tcell_agent.instrumentation.django.database_error_wrapper import instrument_database_error_wrapper
    from django.core.handlers.base import BaseHandler

    old_load_middleware = BaseHandler.load_middleware

    def load_middleware(*args, **kwargs):
        LOGGER.info("Adding middleware")
        _insertMiddleware(
            'tcell_agent.instrumentation.django.middleware.body_filter_middleware.BodyFilterMiddleware')
        _insertMiddleware(
            'tcell_agent.instrumentation.django.middleware.afterauthmiddleware.AfterAuthMiddleware')
        _insertMiddleware(
            'tcell_agent.instrumentation.django.middleware.tcelllastmiddleware.TCellLastMiddleware')
        _insertMiddleware(
            'tcell_agent.instrumentation.django.middleware.tcell_data_exposure_middleware.TCellDataExposureMiddleware',
            atIdx=0)
        _insertMiddleware(
            'tcell_agent.instrumentation.django.middleware.globalrequestmiddleware.GlobalRequestMiddleware',
            atIdx=0)
        _insertMiddleware(
            'tcell_agent.instrumentation.django.middleware.timermiddleware.TimerMiddleware')

        if _dlp_success:
            from tcell_agent.instrumentation.django.dlp import dlp_instrumentation
            dlp_instrumentation()

        if _is_csrf_middleware_enabled():
            instrument_csrf_view_middleware()

        instrument_database_error_wrapper()

        import tcell_agent.instrumentation.django.contrib_auth
        return old_load_middleware(*args, **kwargs)

    BaseHandler.load_middleware = load_middleware


def _get_middleware_index(middleware_list, after=None, before=None, atIdx=None):
    if after:
        return middleware_list.index(after) + 1 if after in middleware_list else len(middleware_list)
    elif before:
        return middleware_list.index(before) if before in middleware_list else 0
    elif atIdx is not None:
        return atIdx
    else:
        return len(middleware_list)


def _insertMiddleware(middleware_class_string, after=None, before=None, atIdx=None):
    from django.conf import settings

    if hasattr(settings, 'MIDDLEWARE') and settings.MIDDLEWARE:
        middleware_list = list(settings.MIDDLEWARE)
        idx = _get_middleware_index(middleware_list, after, before, atIdx)
        middleware_list.insert(idx, middleware_class_string)
        settings.MIDDLEWARE = tuple(middleware_list)
    else:
        middleware_classes_list = list(settings.MIDDLEWARE_CLASSES)
        idx = _get_middleware_index(middleware_classes_list, after, before, atIdx)
        middleware_classes_list.insert(idx, middleware_class_string)
        settings.MIDDLEWARE_CLASSES = tuple(middleware_classes_list)


def _is_csrf_middleware_enabled():
    from django.conf import settings
    if hasattr(settings, 'MIDDLEWARE'):
        if settings.MIDDLEWARE is None:
            return "django.middleware.csrf.CsrfViewMiddleware" in list(settings.MIDDLEWARE_CLASSES)
        else:
            return "django.middleware.csrf.CsrfViewMiddleware" in list(settings.MIDDLEWARE)
    else:
        return "django.middleware.csrf.CsrfViewMiddleware" in list(settings.MIDDLEWARE_CLASSES)


try:
    import django

    if TCellAgent.get_agent():
        try:
            from tcell_agent.instrumentation.django.utils import django15or16

            if django15or16:
                _dlp_success = False
            else:
                from tcell_agent.instrumentation.django.dlp import dlp_instrumentation

                _dlp_success = True
        except ImportError as ie:
            _dlp_success = False
        except Exception as e:
            LOGGER.error("Problem importing DLP: {e}".format(e=e))
            LOGGER.debug(e, exc_info=True)
            _dlp_success = False

        _instrument()
except ImportError as ie:
    pass
except Exception as e:
    LOGGER.debug("Could not instrument django: {e}".format(e=e))
    LOGGER.debug(e, exc_info=True)
