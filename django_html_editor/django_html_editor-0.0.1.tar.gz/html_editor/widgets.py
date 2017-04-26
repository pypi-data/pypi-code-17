from django.forms import Widget
from django.forms.widgets import Textarea
from django.template import loader
from django.utils.safestring import mark_safe


class EditorWidget(Textarea):
    scripts = [
        'html_editor/js/codemirror.js',
        'html_editor/js/formatting.js',
        'html_editor/js/css.js',
        'html_editor/js/xml.js',
        'html_editor/js/javascript.js',
        'html_editor/js/htmlmixed.js',
    ]

    styles = [
        'html_editor/css/codemirror.css',
    ]

    def render(self, name, value, attrs=None):
        template_name = 'html_editor/widget.html'
        context = {
            'name': name,
            'value': value,
            'scripts': self.scripts,
            'styles': self.styles,
        }
        html = loader.render_to_string(template_name, context)
        return mark_safe(html)

