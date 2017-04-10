#!/usr/bin/env python3
# pylint: disable=unused-argument,singleton-comparison

"""PassRestoreControl class."""

import random
import string

import cherrypy

from ..core import cfg
from ..core.templates import templates
from ..db import db
from ..gettext import gettext as _
from ..tools import mail, structural
from .Control import Control
from .User import User


class PassRestoreControl(Control):
    """PassRestoreControl class."""

    __mapper_args__ = {'polymorphic_identity': 'PassRestore'}
    _settings = {'default-placements': ('abovebody',),
                 'one-per-language': True,
                 'node-types': ('article')}
    editMode = None

    @classmethod
    def controlName(cls):
        return _('User password restore form')

    @staticmethod
    def reset_password(user):
        """Password reset request handling."""

        if user.password.startswith('$6$'):
            newpass = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits)
                              for i in range(12))
            user.password = newpass
            message = (_("Dear %s,\n"
                         "As requested by filling in password restoration form, system has\n"
                         "updated your credentials.\n\n"
                         "login: %s\n"
                         "new password: %s\n\n") %
                       (user.name, user.login, newpass))
        else:
            message = (_("Dear %s,\n"
                         "Unfortunately your password is stored in an external database and the form\n"
                         "you've used for password restoration is not able to change it.\n"
                         "If it may be of any use, your login name associated to this e-mail is:\n\n"
                         "   %s\n\n"
                         "Please contact our support team for further assistance.\n\n") %
                       (user.name, user.login))
        mail(cfg.any(('mail', 'password-restore', 'mail'),
                     ('mail', 'automatic-notifications', 'mail')),
             user.email,
             _('Password restoration request processed'),
             message,
             '<html>'+message.replace('\n', '<br />')+'</html>')
        db.commit()
        raise cherrypy.HTTPRedirect('?completed=true')

    @structural
    def fetch(self, placement):
        """Produce constrol's html contents."""

        if cherrypy.request.user:
            raise cherrypy.HTTPRedirect('/')

        if cherrypy.request.params.get('completed', None):
            return _("If information you've provided is valid, your new password "
                     "accompanied by your login name has been sent to the e-mail "
                     "address assigned to your account. If you will not receive "
                     "mail from us within reasonable time, please check your spam "
                     "folder. In case of any further problems, do not hesitate to "
                     "contact our support team directly.")

        elif 'send' in cherrypy.request.params:

            uid = cherrypy.request.params.get('login', '').strip()
            # pylint: disable=singleton-comparison
            user = db.query(User).filter(((User.login == uid) | (User.email == uid)) &
                                         User.active == True).first()
            if user and user.email:
                self.reset_password(user)

            raise cherrypy.HTTPRedirect('?completed=true')
        else:
            return templates['control_password_restore_form'](this=self)
