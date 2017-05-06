# coding: UTF-8

from wtforms import Form, validators
from wtforms.fields import (
    FieldList,
    StringField,
    TextField,
    PasswordField,
    SelectField,
    BooleanField,
    IntegerField
)

from eva.utils.translation import ugettext_lazy as _

from app.blog.settings import MARKUP_CHOICES


class CatalogBaseForm(Form):

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


class CatalogNewForm(CatalogBaseForm):

    name = StringField(_("Name"), validators=[
        validators.DataRequired(),
        validators.Length(min=2, max=128)])


class CatalogEditForm(CatalogBaseForm):
    pass


class ArticleBaseForm(Form):

    category_id = StringField(_("Category ID"))
    catalog_id = StringField(_("Catalog ID"))
    # FIXME: [validators.Optional(), validators.Length(min=8)]
    title = StringField(_("Title"))
    abstract = TextField(_("Abstract"))
    body = TextField(_("Body"))
    body_markup = SelectField(
        _("Body Markup"),
        coerce=int,
        choices=MARKUP_CHOICES,
        validators=[validators.optional()],
        default=1
    )
    is_public = BooleanField(_("Is Public"), default=False)
    tags = FieldList(StringField("Tag ID", [validators.Length(min=8)]))


class ArticleNewForm(ArticleBaseForm):

    title = StringField(_("Title"))
    body = TextField(_("Body"))


class ArticleEditForm(ArticleBaseForm):
    pass


class TagBaseForm(Form):

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


class TagNewForm(TagBaseForm):

    name = StringField(_("Name"), validators=[
        validators.DataRequired(),
        validators.Length(min=2, max=128)])


class TagEditForm(TagBaseForm):
    pass
