# coding: UTF-8

from wtforms import Form, validators
from wtforms.fields import (
    StringField,
    PasswordField,
    SelectField,
    BooleanField,
    IntegerField
)

from eva.utils.translation import ugettext_lazy as _


# TODO: 用户名黑名单验证
class SignInForm(Form):
    """用户登录
    """

    username = StringField(_("Username"), [
        validators.DataRequired(), validators.Length(max=64)])
    password = PasswordField(_("Password"), [
        validators.DataRequired(), validators.Length(max=128)])


class NewIdentifierForm(Form):
    """新建验证码
    """

    type = SelectField(_("Type"), choices=[
        ("email", _("Email")),
    ], default="email")
    data = StringField(_("Data"), [validators.Length(min=2, max=32)])


class SignUpForm(Form):
    """用户注册
    """

    nickname = StringField(_("Nickname"), [validators.Length(min=2, max=32)])
    password = PasswordField(_("Password"), [validators.Length(min=6, max=128)])

    # Identifier
    identifier_id   = StringField(_("Identifier ID"), [validators.UUID()])
    identifier_code = StringField(_("Identifier Code"), [validators.Length(min=3, max=32)])


class ForgetPasswordForm(Form):
    """忘记密码
    """

    password = PasswordField(_("Password"), [validators.Length(min=6, max=128)])

    # Identifier
    identifier_id   = StringField(_("Identifier ID"), [validators.UUID()])
    identifier_code = StringField(_("Identifier Code"), [validators.Length(min=3, max=32)])
