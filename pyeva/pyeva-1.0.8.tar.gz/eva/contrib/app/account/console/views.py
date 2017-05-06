from eva.web import APIRequestHandler, authenticated
from eva.utils.translation import ugettext_lazy as _

from .forms import (
    ProfileEditForm, PasswordResetForm
)


class MyProfile(APIRequestHandler):

    @authenticated
    def get(self):
        '''获取当前会话用户的属性信息
        '''

        self.success(**self.current_user.iowner)

    @authenticated
    def put(self):

        form = ProfileEditForm.from_json(self.get_body_json())
        if not form.validate():
            return self.fail(errors=form.errors)

        user = self.current_user

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

        # TODO: 修改密码是否需要单独，并且提供旧密码？
        if not form.password.is_missing:
            user.set_password(form.password.data)
            # Delete all old sessions, user need resignin.
            for s in user.sessions:
                self.db.delete(s)

        self.db.commit()
        self.success()


class PasswordReset(APIRequestHandler):

    @authenticated
    def put(self):
        '''用户重置密码'''

        user = self.current_user

        form = PasswordResetForm.from_json(self.get_body_json())
        if not form.validate():
            return self.fail(errors=form.errors)

        if not user.check_password(form.old_password.data):
            return self.fail(_("Old password is wrong."))

        user.set_password(form.new_password.data)

        # TODO: 创建新 session , 方便重新登录？
        # Delete all old sessions, user need resignin.
        for s in user.sessions:
            self.db.delete(s)
        self.db.commit()

        self.success()
