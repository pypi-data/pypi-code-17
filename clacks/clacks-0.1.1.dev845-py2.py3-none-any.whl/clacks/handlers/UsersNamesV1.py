#!/usr/bin/env python3

"""/_v1/users-names service handler"""

import cherrypy
from sqlalchemy import func

from ..db import db
from ..models import User
from .URLHandler import URLHandler


class UsersNames(URLHandler):

    """/_v1/users-names service handler"""

    mount_url = '/_v1/users-names'
    dispatcher = 'MethodDispatcher'
    exposed = True

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(any_grant=['USERS_LIST_VIEW',
                                       'USERS_FULL_LIST_VIEW',
                                       'USER_PROFILE_EDIT'])
    def GET(self, suserid=None, *args, **kwargs):

        """Return users."""

        def getNameAndRole(name, surname, company, role):
            """Return name and role as single string (with company as bonus)."""
            result = ''
            if name:
                result += name
            if surname:
                result += ' '+surname
            if company and role:
                result += ' (%s, %s)' % (company, role)
            elif company:
                result += ' ('+company+')'
            elif role:
                result += ' ('+role+')'
            return result.strip()

        record = lambda c: \
            {'id': c.id,
             'name': c.name,
             'surname': c.surname,
             'fullName': ' '.join((c.name, c.surname)),
             'fullNameAndRole': getNameAndRole(c.name, c.surname, c.company, c.role),
             'role': c.role}

        luser = cherrypy.request.user

        if suserid in ('me', 'new'):
            suserid = luser.id

        suser = db.query(User).get(suserid)

        if len(args) == 1:

            c = db.query(User).get(args[0])
            # pylint: disable=too-many-boolean-expressions
            if c and (luser.granted('USERS_FULL_LIST_VIEW') or
                      (c == luser) or luser.isParentOf(c) or
                      (suser == luser and c == luser.parent)):

                return record(c)
            else:
                raise cherrypy.HTTPError(404, 'Record not found')

        if 'fullNameAndRole' in kwargs:
            s = kwargs['fullNameAndRole']

            if s[-1:] == '*':
                s = s[:-1]+'%'
            if s[:1] == '*':
                s = '%'+s[1:]

            r = db.query(User).filter(func.coalesce(User.name, '').concat(' ')
                                      .concat(func.coalesce(User.surname, ''))
                                      .concat(' (')
                                      .concat(func.coalesce(User.company, '')).ilike(s)).all()

            return [record(c) for c in r
                    if (luser.granted('USERS_FULL_LIST_VIEW') or
                        (c == luser) or luser.isParentOf(c) or
                        (suser == luser and c == luser.parent))]
