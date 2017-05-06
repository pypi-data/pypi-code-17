import datetime

from tornado.web import create_signed_value

from eva.web import APIRequestHandler, authenticated
from eva.utils.translation import ugettext_lazy as _
from eva.utils.time_ import rfc3339_string

from .models import (
    User, create_user,
    AuthIdentifier, create_identifier,
    create_session
)
from .forms import (
    NewIdentifierForm, SignUpForm,
    SignInForm,
    ForgetPasswordForm
)
from .utils import identifier_notice_email


class SignUpIdentifier(APIRequestHandler):

    def post(self):
        '''获取注册验证码'''

        form = NewIdentifierForm.from_json(self.get_body_json())
        if not form.validate():
            return self.fail(errors=form.errors)

        t = form.type.data
        d = form.data.data

        c = create_identifier(self.db, t, data=d)

        if t == "email":
            if len(d.split("@")) != 2:
                return self.fail(_("Invalid email address."))
            to_addr = d.strip()
            if self.db.query(User.id).filter_by(email=to_addr).count() > 0:
                return self.fail(_("Email address is existed."))
            identifier_notice_email(to_addr, c.code)
            return self.success(id=c.uuid)
        else:
            return self.fail(_("Unknown identifier type: {}").format(t))


class SignUp(APIRequestHandler):

    def post(self):
        '''完成注册'''

        form = SignUpForm.from_json(self.get_body_json())
        if not form.validate():
            return self.fail(errors=form.errors)

        identifier = self.db.query(AuthIdentifier).filter_by(
            uuid=form.identifier_id.data).first()
        if not identifier:
            return self.fail(_("No such identifier"))

        if identifier.code != form.identifier_code.data:
            return self.fail(_("Invalid identifier code"))

        if not identifier.is_valid():
            return self.fail(_("Identifier is expired"))

        user = self.db.query(User).filter_by(email=identifier.data).first()
        if user:
            # TODO: should not got it!
            return self.fail(_("User is existed"))

        # create user
        user = create_user(self.db,
                           password=form.password.data,
                           email=identifier.data,
                           nickname=form.nickname.data)
        if not user:
            # TODO: more info
            return self.fail(_("Create user failed"))

        # 删除验证码
        self.db.delete(identifier)
        self.db.commit()

        # TODO: 直接返回 sid , 便于用户一步登录？
        self.success()


class SignIn(APIRequestHandler):

    def post(self):
        '''用户登录'''

        form = SignInForm.from_json(self.get_body_json())
        if not form.validate():
            return self.fail(errors=form.errors)

        # support username login
        user = self.db.query(User).filter_by(
            username=form.username.data).first()
        # support email login
        if not user:
            user = self.db.query(User).filter_by(
                email=form.username.data).first()
        # support uid login
        if not user:
            try:
                UID = int(form.username.data)
                user = self.db.query(User).filter_by(uid=UID).first()
            except:
                pass

        if not user:
            return self.fail(_("Wrong username or password"))
        if user.is_locked:
            return self.fail(_("User is locked"))
        if not user.is_active:
            return self.fail(_("User is inactive"))
        if not user.check_password(form.password.data):
            return self.fail(_("Wrong username or password"))

        # 设置其他
        user.last_login = datetime.datetime.utcnow()
        user.last_active = datetime.datetime.utcnow()

        # 验证成功
        session = create_session(
            self.db, user, from_ip=self.request.remote_ip)

        self.require_setting("secret_key", "secure key")
        secret = self.application.settings["secret_key"]
        sid = create_signed_value(
            secret, "Sid", session.sid).decode()  # TODO: fix me!

        self.success(sid=sid, expired=rfc3339_string(session.expired))


class SignOut(APIRequestHandler):

    def get(self):
        '''用户注销'''

        if not self.current_user:
            return self.fail(_("You are not logined!"))

        # TODO: just delete current session!
        # Delete all old sessions, user need resignin.
        for s in self.current_user.sessions:
            self.db.delete(s)
        self.db.commit()

        self.success()


class ForgetPasswordIdentifier(APIRequestHandler):

    def post(self):
        '''获取重置密码验证码'''

        form = NewIdentifierForm.from_json(self.get_body_json())
        if not form.validate():
            return self.fail(errors=form.errors)

        t = form.type.data
        d = form.data.data

        c = create_identifier(self.db, t, data=d)

        if t == "email":
            if len(d.split("@")) != 2:
                return self.fail(_("Invalid email address."))
            to_addr = d.strip()
            u = self.db.query(User.id).filter_by(email=to_addr).first()
            if not u:
                return self.fail(_("Email address is not registered."))
            identifier_notice_email(to_addr, c.code)
            return self.success(id=c.uuid)
        else:
            return self.fail(_("Unknown identifier type: {}").format(t))


class ForgetPassword(APIRequestHandler):

    def post(self):
        '''完成重置密码'''

        form = ForgetPasswordForm.from_json(self.get_body_json())
        if not form.validate():
            return self.fail(errors=form.errors)

        identifier = self.db.query(AuthIdentifier).filter_by(
            uuid=form.identifier_id.data).first()
        if not identifier:
            return self.fail(_("No such identifier"))

        if identifier.code != form.identifier_code.data:
            return self.fail(_("Invalid identifier code"))

        if not identifier.is_valid():
            return self.fail(_("Identifier is expired"))

        u = self.db.query(User).filter_by(email=identifier.data).first()
        if not u:
            # TODO: should not got it!
            return self.fail(_("User is not existed"))

        u.set_password(form.password.data)

        self.db.delete(identifier)
        for s in u.sessions:
            self.db.delete(s)

        self.db.commit()

        # TODO: 生成新 sid ， 以便用户自动登录？
        self.success()
