#!/usr/bin/env python3

""" grants definitions required by GtCMS core.cms module """

from ..gettext import gettext as _

grants = {
    'INHERITED': {
        'description':
        _('used for marking that page should use the same grant '
          'for a given operation as the parent page, '
          'it need not be given to users directly'),
        'internal': True
    },
    'ANONYMOUS': {
        'description':
        _('used for marking that page should be available for anonymous access'),
        'internal': True
    },
    'AUTHORIZED': {
        'description':
        _('used for marking that page should be available for any authorized user;'
          'in the future will also mean that user can login to the system'),
        'internal': False
    },
    'SITE_ADMIN': {
        'description':
        _('gives full administrator rights to the whole service '
          'also implicitly gives all other possible grants in most scenarios'),
    },
    'SITE_STRUCTURE_VIEW': {
        'description':
        _('gives access to view of whole site structure'),
    },
    'USERS_LIST_VIEW': {
        'description':
        _('gives access to users list view (usually only users for which given user has supervisor role)'),
    },
    'USERS_FULL_LIST_VIEW': {
        'description':
        _('gives access to users list (whole list)'),
    },
    'LOGIN_HISTORY_VIEW': {
        'description':
        _('gives access to login history graphs'),
    },
    'DEVELOPMENT': {
        'description':
        _('gives access to developent system features; do not use on production system!'),
        'internal': True
    },
    'USER_PROFILE_EDIT': {
        'description':
        _('gives user access to administration panel form to manage account details'),
    },
    'USER_CONFIRMED_DATA': {
        'description':
        _('set automatically when user clicks e-mailed activation link'),
    },
    'FILE_MANAGEMENT': {
        'description':
        _('enables access to static files browsing upload and removal')
    }
}
