from django.forms import ModelForm
from html_editor.widgets import EditorWidget

def admin_editor(fields):
    if type(fields) != list:
        raise TypeError('list type expected for argument fields')

    def admin_decorator(cls):
        class AdminForm(ModelForm):
            def __init__(self, *args, **kwargs):
                super(AdminForm, self).__init__(*args, **kwargs)
                for f in fields:
                    self.fields[f].widget = EditorWidget()

        class AdminWrapper(cls):
            form = AdminForm

        return AdminWrapper

    return admin_decorator
