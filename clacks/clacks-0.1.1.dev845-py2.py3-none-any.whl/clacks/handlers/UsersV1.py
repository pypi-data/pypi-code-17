#!/usr/bin/env python3
# pylint: disable=too-many-branches,too-many-statements,singleton-comparison

""" /_v1/users service handler."""

import json

import cherrypy
from sqlalchemy import func
from sqlalchemy.orm import joinedload, undefer

from .. import models
from ..core import ROOTPATH, cfg
from ..core.templates import templates
from ..db import db
from ..gettext import gettext as _
from ..models import User, UserAddress
from ..tools import mail
from .URLHandler import URLHandler


class Users(URLHandler):
    """ /_v1/users service handler."""

    mount_url = '/_v1/users'
    dispatcher = 'MethodDispatcher'
    exposed = True

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(any_grant=['USERS_LIST_VIEW', 'USER_PROFILE_EDIT'])
    def GET(self, uid=None, *, sort=None, parent=None, **kwargs):

        """produce users list with json compatible content."""

        export = lambda c: {
            'id': c.id,
            'name': c.name,
            'login': c.login,
            'surname': c.surname,
            'company': c.company,
            'fullName': ' '.join((c.name, c.surname)) if c.name and c.surname else '',
            'walletAmount': float(c.wallets[0].balance) if hasattr(c, 'wallets') and len(c.wallets) else 0,
            'created': str(c.created)[:10],
            'active': c.active or False,
            'lastLogin': str(c.loginDates[-1].timestamp)[:19] if len(c.loginDates) else None,
            'hasChildren': c.dependantsCount,
            'role': c.role
        }

        admin = cherrypy.request.user

        if uid is not None:

            if uid in ('me', admin.id):
                c = admin
            elif admin.granted('USERS_LIST_VIEW'):
                c = db.query(User).get(uid)

            if c is not None and (admin.granted('SITE_ADMIN') or
                                  (admin == c) or
                                  admin.isParentOf(c)):
                return c.export()
            else:
                raise cherrypy.HTTPError(404, 'Record not found')
        else:
            if admin.granted('SITE_ADMIN'):
                q = db.query(User)
            elif admin.granted('USERS_LIST_VIEW'):
                q = admin.allDependantsAndMe
            else:
                q = q.filter_by(id=admin.id)

            q = q.options(undefer('dependantsCount'), joinedload('loginDates'))

            if hasattr(models, 'Wallet'):
                q = q.options(joinedload('wallets').undefer('balance'))

            if 'filter' in kwargs:
                s = kwargs.pop('filter')

                if s[-1:] == '*':
                    s = s[:-1]+'%'
                    if s[:1] == '*':
                        s = '%'+s[1:]

                q = q.filter(User.login.concat(' ')
                             .concat(User.name).concat(' ')
                             .concat(User.surname)
                             .concat(' ')
                             .concat(func.coalesce(User.company, ''))
                             .concat(' ')
                             .concat(User.email)
                             .ilike(s))

            if parent is not None:
                if parent.isdecimal():
                    q = q.filter(User._parent == parent)
                elif admin.granted('SITE_ADMIN'):
                    q = q.filter(User._parent.is_(None))
                else:
                    q = db.query(User).filter_by(id=admin.id)

            if sort is not None and sort[1:] == 'created':
                if sort[0] != '-':
                    q = q.order_by(User.created.asc(), User.id)
                else:
                    q = q.order_by(User.created.desc(), User.id)
            elif sort is not None and sort[1:] == 'login':
                if sort[0] != '-':
                    q = q.order_by(User.login.asc(), User.id)
                else:
                    q = q.order_by(User.login.desc(), User.id)
            elif sort is not None and sort[1:] == 'company':
                if sort[0] != '-':
                    q = q.order_by(User.company.asc(), User.id)
                else:
                    q = q.order_by(User.company.desc(), User.id)
            elif sort is not None and sort[1:] == 'active':
                if sort[0] != '-':
                    q = q.order_by(User.active.asc(), User.created.asc(), User.id)
                else:
                    q = q.order_by(User.active.desc(), User.created.desc(), User.id)
            else:
                if sort == '-fullName':
                    q = q.order_by(User.surname.desc(), User.name.desc(), User.id.desc())
                else:
                    q = q.order_by(User.surname, User.name, User.id)

            return [export(c) for c in q.http_range()]

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(any_grant=['USERS_LIST_VIEW', 'USER_PROFILE_EDIT'])
    def PUT(self, uid=None):  # pylint: disable=too-many-locals,too-many-branches

        """Update User data"""

        import random
        import string

        data = json.loads(cherrypy.request.body.read().decode())

        if uid == 'me':
            uid = cherrypy.request.user.id
            data['id'] = cherrypy.request.user.id
        elif uid is None or int(uid) != data['id']:
            cherrypy.HTTPError(400, 'Bad syntax')

        user = db.query(User).get(data['id'])

        if '_parent' in data:
            if data['_parent'] and len(data['_parent']):
                data['_parent'] = int(data['_parent'])
            else:
                data.pop('_parent', None)
                user._parent = None

        if ('_parent' in data) and (int(data['_parent']) > 0):
            parent = db.query(User).get(data['_parent'])
            if not parent:
                cherrypy.HTTPError(400, _('Błędna wartość dla pola użytkownika nadrzędnego'))
            # to prevent dependency loops:
            elif user.allDependantsAndMe.filter_by(id=data['_parent']).count():
                cherrypy.HTTPError(400, _('Błędna wartość dla pola użytkownika nadrzędnego'))

        for field in ['email', 'password', 'name', 'surname', 'active', 'phone', 'newsletter', 'vatid',
                      'login', 'fax', 'company', 'cellphone', 'wantsVatInvoice',
                      'role', '_parent']:
            if field in data:
                setattr(user, field, data[field])

        if 'addresses' in data:
            for addr in user.addresses:
                if addr.id not in [a['id'] for a in data['addresses'] if 'id' in a]:
                    user.addresses.remove(addr)

            for addr in data['addresses']:
                if 'id' in addr and addr['id'] not in [a.id for a in user.addresses]:
                    addr.pop('id')
                if 'id' in addr:
                    db.query(UserAddress).get(addr['id']).update(**addr)
                else:
                    user.addresses.append(UserAddress(**addr))

        if data.get('activationMail', False):
            newpass = ''.join(random.choice(string.ascii_letters) for a in range(16))
            user.password = newpass

            mailvars = {'domain': ROOTPATH.name,
                        'password': newpass}

            mail(cfg.get('mail', 'shop', 'mail'),
                 user.email,
                 'Twoje konto w serwisie %s zostało aktywowane' % ROOTPATH.name,
                 templates['body_account_activated_mail_plain'](**mailvars),
                 templates['body_account_activated_mail_html'](**mailvars))

        db.commit()

        return self.GET(uid)

    @cherrypy.tools.json_out()
    @cherrypy.tools.require(grant='USERS_LIST_VIEW')
    def POST(self):

        """Create a new User"""

        data = json.loads(cherrypy.request.body.read().decode())

        if 'id' in data:
            cherrypy.HTTPError(400, 'Bad request')

        # TODO: this code needs fixing to force setting parent depending on user grants
        if '_parent' in data and data['_parent']:
            data['_parent'] = int(data['_parent'])
        else:
            data['_parent'] = cherrypy.request.user.id

        if '_parent' in data and int(data['_parent']) > 0:
            parent = db.query(User).get(data['_parent'])
            if not parent:
                cherrypy.HTTPError(400, _('Błędna wartość dla pola użytkownika nadrzędnego'))
        user = User()

        for field in ['email', 'password', 'name', 'surname', 'active', 'phone',
                      'newsletter', 'vatid', 'login', 'country', 'fax',
                      'company', 'cellphone', 'wantsVatInvoice', 'role', '_parent']:
            if field in data:
                setattr(user, field, data[field])

        # TODO: adding wallet needs cleaner implementation, but for now:
        try:
            from ..models import Wallet
            user.wallets.append(Wallet(currency='PLN'))
        except ImportError:
            pass
        user.role = 'klient'  # TODO: config option? better yet - drop roles altogether
        db.add(user)
        db.commit()

        return self.GET(user.id)
