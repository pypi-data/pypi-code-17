from eva.web import APIRequestHandler, administrator
from eva.utils.translation import ugettext_lazy as _
from eva.sqlalchemy.list import admin_list_objects

from eva.contrib.app.auth.models import User

from .forms import (
    ProfileEditForm, PasswordResetForm
)


class _SingleUserBaseHandler(APIRequestHandler):

    @administrator
    def prepare(self):
        self.user = self.db.query(User).filter_by(uid=self.path_args[0]).one()


class SingleUserProfileHandler(_SingleUserBaseHandler):

    def get(self, uid):
        '''获取用户信息
        '''

        self.success(**self.user.iadmin)

    def put(self, uid):

        form = ProfileEditForm.from_json(self.get_body_json())
        if not form.validate():
            return self.fail(errors=form.errors)

        user = self.user

        if not form.nickname.is_missing:
            user.nickname = form.nickname.data
        if not form.first_name.is_missing:
            user.first_name = form.first_name.data
        if not form.last_name.is_missing:
            user.last_name = form.last_name.data
        if not form.gender.is_missing:
            user.gender = {
                'male': 1, 'female': 2, 'secret': 0}.get(form.gender.data, 0)
        if not form.language.is_missing:
            user.language = form.language.data

        self.db.commit()
        self.success()


class SingleUserPasswordHandler(_SingleUserBaseHandler):

    def put(self):
        '''重置用户密码'''

        user = self.user

        form = PasswordResetForm.from_json(self.get_body_json())
        if not form.validate():
            return self.fail(errors=form.errors)

        user.set_password(form.password.data)

        # TODO: 创建新 session , 方便重新登录？
        # Delete all old sessions, user need resignin.
        for s in user.sessions:
            self.db.delete(s)
        self.db.commit()

        self.success()


class SingleUserHandler(_SingleUserBaseHandler):

    def get(self, uid):
        '''查看用户'''
        # TODO
        self.success(**self.user.iadmin)

    def delete(self, uid):
        '''删除用户'''
        # 只能设置用户为已删除状态
        pass


class UserHandler(APIRequestHandler):

    @administrator
    def get(self):
        '''查看用户列表'''

        q = self.db.query(User)
        d = admin_list_objects(self, User, q)
        self.success(**d)

    @administrator
    def post(self):
        '''创建新用户'''
        pass
