from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from cl_utils.widgets import SelectWithOtherWidget

class ChoiceWithOtherField(forms.MultiValueField):
    '''
    A choice field with a "free entry" option.
    '''
    _choices = []
    choice_field = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        self.other_value = kwargs.pop('other_value', '-1')
        self.other_label = kwargs.pop('other_label', _(u'Other'))
        self.choices = kwargs.pop('choices', [])

        self._was_required = kwargs.pop('required', True)
        kwargs['required'] = False

        fields = [
            self.choice_field,
            forms.CharField()
        ]
        widget = SelectWithOtherWidget(other_value=self.other_value)
        super(ChoiceWithOtherField, self).__init__(fields=fields, widget=widget, *args, **kwargs)

    def _get_choices(self):
        return self._choices

    def _set_choices(self, value):
        self._choices = self.widget.choices = self.choice_field.choices = list(value) + [(self.other_value, self.other_label)]

    choices = property(_get_choices, _set_choices)

    def compress(self, data_list):
        if 0 == len(data_list):
            if self._was_required:
                raise ValidationError(self.error_messages['required'])
            else:
                return None

        if data_list[0] == self.other_value:
            return data_list[1]
        return data_list[0]

    def validate(self, value):
        if self._was_required and value in validators.EMPTY_VALUES:
            raise ValidationError(self.error_messages['required'])

    def prepare_initial(self, initial, name):
        choice_field_name = '%s_0' %name
        char_field_name = '%s_1' % name
        if initial.get(choice_field_name, self.other_value) == self.other_value:
            initial[name] = initial.get(char_field_name, None)
        else:
            initial[name] = initial.get(choice_field_name)
