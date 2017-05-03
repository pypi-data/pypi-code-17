def as_some_renderer(form):
    return form._html_output(
        normal_row=u"""<div class="field"><div %(html_class_attr)s>%(label)s %(errors)s <div class="helptext">%(help_text)s</div> %(field)s</div></div>""",
        error_row=u"%s",
        row_ender="</div>",
        help_text_html=u"%s",
        errors_on_separate_row=False
    )
