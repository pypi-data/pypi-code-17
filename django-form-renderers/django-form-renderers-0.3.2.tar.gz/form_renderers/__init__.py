from django.conf import settings


SETTINGS = {"enable-bem-classes": False, "replace-as-p": False, "replace-as-table": False}
try:
    SETTINGS.update(settings.FORM_RENDERERS)
except AttributeError:
    pass


def as_div(form):
    """This formatter arranges label, widget, help text and error messages by
    using divs."""

    form.error_css_class = "Field-message--error"

    if SETTINGS["enable-bem-classes"]:
        return form._html_output(
            normal_row=u"""<div%(html_class_attr)s>%(label)s<div class="Field-item">%(errors)s %(field)s</div><div class="Field-message">%(help_text)s</div></div>""",
            error_row=u"%s",
            row_ender="</div>",
            help_text_html=u"%s",
            errors_on_separate_row=False
        )
    else:
        return form._html_output(
            normal_row=u"""<div class="field"><div %(html_class_attr)s>%(label)s %(errors)s %(field)s</div><div class="helptext">%(help_text)s</div></div>""",
            error_row=u"%s",
            row_ender="</div>",
            help_text_html=u"%s",
            errors_on_separate_row=False
        )
