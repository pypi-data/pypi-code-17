# coding: UTF-8

from eva.conf import settings
from eva.utils.translation import ugettext_lazy as _

from wtforms import Form, validators
from wtforms.fields import (
    StringField,
    PasswordField,
    SelectField,
    BooleanField,
    IntegerField
)

from eva.contrib.app.auth.models import GENDER_CHOICES


class ProfileEditForm(Form):
    """更新用户属性表单
    """

    nickname = StringField(_("Nickname"))
    first_name = StringField(_("First Name"))
    last_name = StringField(_("Last Name"))
    gender = SelectField(_('Gender'), choices=GENDER_CHOICES, default="secret")
    language = SelectField(_('Language'), choices=settings.LANGUAGES, default="en")
    password = PasswordField(_("Password"))


class PasswordResetForm(Form):
    """用户重置自己的密码
    """

    old_password = PasswordField(_("Old Password"), [
        validators.DataRequired(),
        validators.Length(min=6, max=64)])
    new_password = PasswordField(_("New Password"), [
        validators.DataRequired(),
        validators.Length(min=6, max=64)])
