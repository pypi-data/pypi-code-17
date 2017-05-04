"""
Extra HTML Widget classes based on django.forms.extra.widgets.SelectDateWidget
BUT the fields are in an other order: dd/mm/yyyy)


/============[ DEPRECATED! NOW USE THE FOLLOWING: ]================\
|                                                                  |
|                                                                  |

# settings.py
USE_L10N = True


# forms.py
class MyForm(forms.ModelForm):
    birthdate = forms.DateField(widget=SelectDateWidget(years=xrange(1900, 2009), required=False),
            initial=None, label=_('Birth date'), required=True)

|                                                                  |
\__________________________________________________________________/
"""


import datetime
import re

from django import forms
from django.forms.widgets import Widget, Select
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe

__all__ = ('SelectDateWidget',)

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')

class SelectDateWidget(Widget):
    """
    A Widget that splits date input into three <select> boxes.
    """
    day_field = '%s_day'
    month_field = '%s_month'
    year_field = '%s_year'

    def __init__(self, attrs=None, years=None):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year+10)

    def render(self, name, value, attrs=None):
        try:
            year_val, month_val, day_val = value.year, value.month, value.day
        except AttributeError:
            year_val = month_val = day_val = None
            if isinstance(value, basestring):
                match = RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val = [int(v) for v in match.groups()]

        output = []

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        local_attrs = self.build_attrs(id=self.month_field % id_)

        day_choices = [(i, i) for i in range(1, 32)]
        local_attrs['id'] = self.day_field % id_
        select_html = Select(choices=day_choices).render(self.day_field % name, day_val, local_attrs)
        output.append(select_html)

        month_choices = MONTHS.items()
        month_choices.sort()
        local_attrs['id'] = self.month_field % id_
        select_html = Select(choices=month_choices).render(self.month_field % name, month_val, local_attrs)
        output.append(select_html)

        year_choices = [(i, i) for i in self.years]
        local_attrs['id'] = self.year_field % id_
        select_html = Select(choices=year_choices).render(self.year_field % name, year_val, local_attrs)
        output.append(select_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_month' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        y, m, d = data.get(self.day_field % name), data.get(self.month_field % name), data.get(self.year_field % name)
        if y and m and d:
            return '%s-%s-%s' % (d, m, y)
        return data.get(name, None)


class SelectWithOtherWidget(forms.MultiWidget):
    '''
    A select widget with an "other" charfield.

    To be used together with cl_utils.fields.ChoiceWithOtherField.
    '''
    _choices = []
    select_widget = None

    def __init__(self, other_value='-1'):
        self.other_value = other_value
        self.select_widget = forms.Select(choices=self.choices)
        widgets = [
            self.select_widget,
            forms.TextInput()
        ]
        super(SelectWithOtherWidget, self).__init__(widgets)

    def _get_choices(self):
        return self._choices

    def _set_choices(self, choices):
        self._choices = self.widgets[0].choices = choices
    choices = property(_get_choices, _set_choices)

    def decompress(self, value):
        if not value:
            return [None, None]
        if value not in dict(self.choices).keys():
            return [self.other_value, value]
        return [value, None]
