from itertools import chain
from django.forms import Select, DateInput
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape, format_html, format_html_join
from django.forms import widgets as dj_widgets
from django.template import Context, loader

try:
    from django.forms import util as form_utils
except ImportError:
    from django.forms import utils as form_utils


class SelectCallback(Select):
    def __init__(self, attrs=None):
        super(Select, self).__init__(attrs)
        self.choices_callback = None

    def render(self, name, value, attrs=None):
        self.choices = list(self.choices_callback())
        return super(SelectCallback, self).render(name, value, attrs)


class DatePickerWidget(DateInput):
    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(DatePickerWidget, self).build_attrs(extra_attrs, **kwargs)
        attrs['class'] = attrs.get('class', '') + ' date-picker'
        attrs['data-date-autoclose'] = 'true'
        attrs['data-date-format'] = self.format.replace('y', 'yy')\
            .replace('Y', 'yyyy')\
            .replace('M', 'mm')\
            .replace('D', 'dd')\
            .replace('%', '')
        return attrs


class LabelWidget(Select):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''

        final_attrs = self.build_attrs(attrs, name=name)
        id_ = final_attrs.get('id', '')

        label_attrs = self.build_attrs(
            {'id': '%s_label' % id_,
             'class': 'label_widger'},
            **final_attrs)

        out_str = format_html(u'<span{0}>', form_utils.flatatt(label_attrs))

        if len(self.choices) > 0:
            for option_value, option_label in chain(self.choices, choices):
                if option_value == value:
                    out_str += form_utils.format_html(u'<span>{0}</span>', option_label)
        else:
            out_str += conditional_escape(form_utils.force_text(value))

        out_str += mark_safe(u'</span>')

        input_attrs = self.build_attrs(
            {'type': 'hidden',
             'value': form_utils.force_text(value)},
            **final_attrs)

        out_str += form_utils.format_html(u'<input{0} />', form_utils.flatatt(input_attrs))
        return out_str


class RadioFieldRendererTemplated(dj_widgets.RadioFieldRenderer):
    def render(self):
        c = Context({'render': self})
        t = loader.get_template('ua2.forms/radio.html')
        return t.render(c)


class RadioSelectTemplated(dj_widgets.RadioSelect):
    renderer = RadioFieldRendererTemplated
