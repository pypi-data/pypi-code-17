# coding: UTF-8

from wtforms import Form, validators
from wtforms.fields import (
    StringField,
    TextField,
    PasswordField,
    SelectField,
    BooleanField,
    IntegerField
)

from eva.utils.translation import ugettext_lazy as _

from app.blog.settings import MARKUP_CHOICES


class CategoryBaseForm(Form):

    parent_id = StringField(_("Parent ID"))
    name = StringField(_("Name"))
    summary = TextField(_("Summary"))
    body = TextField(_("Body"))
    body_markup = SelectField(
        _("Body Markup"),
        coerce=int,
        choices=MARKUP_CHOICES,
        validators=[validators.optional()],
        default=1
    )


class CategoryNewForm(CategoryBaseForm):

    name = StringField(_("Name"), validators=[
        validators.DataRequired(),
        validators.Length(min=2, max=128)])


class CategoryEditForm(CategoryBaseForm):
    pass
