# Author: Jonathan Slenders, City Live

from django.forms.fields import DateField, SplitDateTimeField
from django.forms.widgets import DateInput, SplitDateTimeWidget
from django.utils import translation
from django.utils.safestring import mark_safe


DATE_INPUT_FORMATS = {
    'nl': ('%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d'), # 25/10/2006, 25/10/06, '2006-10-25'
    'fr': ('%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d'), # 25/10/2006, 25/10/06, '2006-10-25'
    'en': ('%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d'), # 10/25/2006, 10/25/06, '2006-10-25'
    'en-us': ('%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d'), # 10/25/2006, 10/25/06, '2006-10-25'
}

AJAX_DATE_FORMAT = {
    'nl': 'dd/mm/yy',
    'fr': 'dd/mm/yy',
    'en-us': 'mm/dd/yy',
    'en': 'mm/dd/yy',
}

TIME_INPUT_FORMATS = ('%H:%M:%S', '%H:%M' )

class AjaxDateInput(DateInput):
    def __init__(self, *args, **kwargs):
        kwargs['format'] = DATE_INPUT_FORMATS [ translation.get_language() ][0]
        DateInput.__init__(self, *args, **kwargs)

    def _get_script(self, id):
        format = AJAX_DATE_FORMAT [translation.get_language() ]

        return mark_safe(
            "<script type=\"text/javascript\">"
            "$(document).ready(function(){ "
            "     $('#%s').datepicker({dateFormat: '%s'});"
            "});"
            "</script>"
             % (id, format))

    def render(self, name, value, attrs=None):
        result = DateInput.render(self, name, value, attrs=attrs)
        result += self._get_script(id=attrs['id'])
        return result


class AjaxDateField(DateField):
    """
    Date field which supports nl/fr/en internationalisation
    and an Ajax date picker.
    """
    widget = AjaxDateInput

    def __init__(self, *args, **kwargs):
        input_formats = DATE_INPUT_FORMATS [translation.get_language() ]

        DateField.__init__(self, input_formats=input_formats, *args, **kwargs)


class AjaxDateTimeInput(SplitDateTimeWidget):
    def __init__(self, *args, **kwargs):
        kwargs['date_format'] = DATE_INPUT_FORMATS [ translation.get_language() ][0]
        kwargs['time_format'] = TIME_INPUT_FORMATS [0]
        SplitDateTimeWidget.__init__(self, *args, **kwargs)


    def _get_script(self, id):
        date_format = AJAX_DATE_FORMAT [translation.get_language() ]

        return mark_safe(
            "<script type=\"text/javascript\">"
            "$(document).ready(function(){ "
            "     $('#%s_0').datepicker({dateFormat: '%s'});"
            "     $('#%s_1').timePicker(); "
            "});"
            "</script>"
             % (id, date_format, id))

    def render(self, name, value, attrs=None):
        result = SplitDateTimeWidget.render(self, name, value, attrs=attrs)
        result += self._get_script(id=attrs['id'])
        return result


class AjaxDateTimeField(SplitDateTimeField):
    """
    DateTime field which supports nl/fr/en internationalisation
    and an Ajax date picker. (Has individual text boxes for date and time.)
    """
    widget = AjaxDateTimeInput

    def __init__(self, *args, **kwargs):
        input_date_formats = DATE_INPUT_FORMATS [translation.get_language() ]
        input_time_formats = TIME_INPUT_FORMATS

        SplitDateTimeField.__init__(self, input_date_formats=input_date_formats,
                input_time_formats=input_time_formats, *args, **kwargs)


