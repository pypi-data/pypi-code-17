import json
from typing import List

from django.forms.utils import flatatt
from django.forms.widgets import HiddenInput
from django.template.loader import render_to_string
from django.utils.encoding import force_text


class Columns(List):
    """A list that contains information about the columns

    It includes one extra 'widgets' function that returns a flat
    list of all the rendered widgets to be used in the template.
    """
    def widgets(self):
        return [c['widget'] for c in self]

    def add(self, name, widget, label):
        """Adds a column to the list"""
        self.append({
            'name': name,
            'widget': widget,
            'label': label
        })


class StructJSONInput(HiddenInput):
    class Media:
        js = ('js/structjsonfield.js', )
        css = {
            'all': ('css/structjsonfield.css', )
        }

    def __init__(self, structure, add_label, *args, **kwargs):
        self.structure = structure
        self.add_label = add_label
        super(StructJSONInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self.format_value(value))

        disabled = attrs.get('disabled', False)

        columns = Columns()
        default_widget_attrs = {'disabled': disabled}

        for fieldname, column in self.structure.items():
            widget_attrs = column.widget.attrs.copy()
            widget_attrs.update(default_widget_attrs)
            columns.add(name=fieldname,
                        widget=column.widget.render(fieldname, '', widget_attrs),
                        label=column.label)

        context = {
            'id': attrs['id'],
            'disabled': disabled,
            'input_attrs': flatatt(final_attrs),
            'target_id': 'target_{}'.format(name),
            'template_id': 'template_{}'.format(name),
            'add_label': self.add_label,
            'name': name,
            'columns': columns,
            # 'input_value': json.dumps(value),
            'value': value,
            'unpacked': self._unpack(value, default_widget_attrs)
        }

        return render_to_string('structjsonfield/widget.html', context)

    def format_value(self, value):
        return json.dumps(value)

    def _unpack(self, value, default_widget_attrs={}):
        unpacked = []
        for line in value:
            line_unpacked = []
            for key, value in line.items():
                widget = self.structure[key].widget
                attrs = widget.attrs.copy()
                attrs.update(default_widget_attrs)
                line_unpacked.append(widget.render(key, value, attrs))
            unpacked.append(line_unpacked)
        return unpacked
