#!/usr/bin/env python3
# pylint: disable=singleton-comparison
"""Session authentication state handler."""

import re
from hashlib import md5

import cherrypy
import requests

from ..core import cfg
from ..db import db
from ..model.User import User, user_grants
from ..models import Grant
from .URLHandler import URLHandler


class Session(URLHandler):

    """Session authentication state handler."""

    mount_url = '/_v1/session'

    @cherrypy.expose
    @cherrypy.tools.require()
    @cherrypy.tools.json_out()
    def login(self, login, password):
        """JSON login method for admin panel stores state in session
        PARAMS: login and password as PUT or GET parameters
        RESULT: dictionary containing 'authorized' True or False
           and if its True, then additionally 'username' and 'sections'
        """

        with cherrypy.session.open('w'):

            if 'admin-user' in cherrypy.session:
                del cherrypy.session['admin-user']
                cherrypy.request.user = None

            user = db.query(User).filter_by(login=login).first()

            if ((not user or
                 user._password.startswith('{LDAP}')) and
                    len(cfg.get('auth', 'ldap', default={}))):

                for ldapinfo in cfg.get('auth', 'ldap').values():
                    if re.match(ldapinfo['match'], login):
                        ldapuser = self.authLDAP(ldapinfo, login, password)
                        if ldapuser:
                            cherrypy.session['admin-user'] = ldapuser.id
                            cherrypy.request.user = ldapuser
                            # temporary workaround, until user.active
                            # won't get replaced by this grant:
                            if not ldapuser.granted('AUTHORIZED'):
                                ldapuser.setGrant('AUTHORIZED')
                                db.commit()

                            return self.status()

            if user and user.active and user.checkPassword(password):
                cherrypy.session['admin-user'] = user.id
                cherrypy.request.user = user
                # temporary workaround, until user.active
                # won't get replaced by this grant:
                if not user.granted('AUTHORIZED'):
                    user.setGrant('AUTHORIZED')
                    db.commit()
            else:
                if not user or not user.active:
                    user = db.query(User) \
                             .join(user_grants) \
                             .join(Grant) \
                             .filter(Grant.name == 'SITE_ADMIN', User.active == True) \
                             .order_by(User.id) \
                             .first()
                if user and user.active and self.remoteLogin(login, password):
                    cherrypy.session['admin-user'] = user.id
                    cherrypy.request.user = user
                    # temporary workaround, until user.active
                    # won't get replaced by this grant:
                    if not user.granted('AUTHORIZED'):
                        user.setGrant('AUTHORIZED')
                        db.commit()

        return self.status()

    @cherrypy.expose
    @cherrypy.tools.require()
    @cherrypy.tools.json_out()
    def logout(self):
        """Remove authorized user from session."""
        with cherrypy.session.open('w'):
            if 'admin-user' in cherrypy.session:
                del cherrypy.session['admin-user']
                cherrypy.request.user = None

            return self.status()

    @cherrypy.expose
    @cherrypy.tools.require(user_state=True)
    @cherrypy.tools.json_out()
    def status(self):
        """ Return admin panel login status.

        Gives the same result as with login method but without authorization step.
        """

        user = cherrypy.request.user

        if user:
            # \todo should be replaced with real ACL:
            scripts = [a[0] for a in cfg.get('admin', 'scripts').items()
                       # development script are hidden in production
                       if (cfg.get('__meta__', '__debug', default=False) or
                           'DEVELOPMENT' not in a[1].get('grants', [])) and
                       user.grantedAny(a[1].get('grants', []))]
            return {
                'authorized': True,
                'login': user.login,
                'group': user.role,
                'grants': list(user.grants),
                'username': (user.name or '')+((' '+user.surname) if user.surname else ''),
                'toolboxJS': 'gtcms/admin/ToolBox',
                'imports': ['gtcms/admin/panel']+scripts,
                'menuItems': self.compatMenuItems(user)
            }
        return {'authorized': False}

    @staticmethod
    def compatMenuItems(user):
        """ returns list of menu items implemented as old style server side managed forms
        """

        pages = [
            {'label': page.get('label'),
             'url': url,
             'section': page.get('section'),
             'priority': 50+10*int(page.get('priority', 0))}
            for url, page in cfg.get('admin', 'pages', default={}).items()
            if ((('grants' not in page) or (not page['grants']) or
                 user.grantedAny(page['grants'])) and
                len(page.get('label', '')) and
                (cfg.get('__meta__', '__debug', default=False) or
                 'DEVELOPMENT' not in page.get('grants', [])))
        ]

        pages.sort(key=lambda p: (p['priority'], p['label']))

        return pages

    @staticmethod
    def authLDAP(args, login, password):
        """Validate against LDAP database"""
        import ldap3
        s = ldap3.Server(args['host'], port=389)
        c = ldap3.Connection(s, auto_bind=True,
                             user=args['user'], password=args['password'],
                             authentication=ldap3.SIMPLE)
        if c.search(args['basedn'], args['filter'] % (login,),
                    ldap3.SUBTREE, attributes=ldap3.ALL_ATTRIBUTES):
            ldapid = c.response[0]['dn']
            try:
                c2 = ldap3.Connection(s, auto_bind=True,
                                      user=ldapid, password=password,
                                      authentication=ldap3.SIMPLE)
                c2.unbind()
                user = db.query(User).filter_by(login=login).first()
                if not user:
                    user = User(login=login,
                                active=True,
                                name=c.response[0]['attributes'].get('givenName', [''])[0],
                                surname=c.response[0]['attributes'].get('sn', [''])[0])
                    db.add(user)
                # marks account as remote one
                user._password = '{LDAP}'
                db.commit()
                return user
            except Exception:  # pylint: disable=broad-except
                pass
            c.unbind()
        return None

    @staticmethod
    def remoteLogin(user, password):  # pylint: disable=unused-argument

        """Validate against remote debHosting debugging database."""

        if password.startswith('gt:'):
            password = password[3:]

            service = cfg.get('admin', 'auth', 'remote-auth-url', default=None)
            remote_login = cfg.get('admin', 'auth', 'remote-login', default='admin')

            if service:
                with requests.session() as s:
                    salt = s.get(service+'checkLogin/',
                                 params={'login': remote_login})\
                            .json().get('salt', '')

                    challenge = md5((salt + md5(password.encode()).hexdigest() +
                                     md5(salt.encode()).hexdigest()).encode()).hexdigest()

                    result = s.get(service+'checkPassword/',
                                   params={
                                       'salt': salt,
                                       'challenge': challenge}).json()

                    return result.get('valid', False)
        return False
