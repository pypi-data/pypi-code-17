''' Copied from http://lazypython.blogspot.com/2008/12/building-read-only-field-in-django.html '''

from django import forms
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe

class ReadOnlyWidget(forms.Widget):
    def render(self, name, value, attrs):
        final_attrs = self.build_attrs(attrs, name=name)
        if hasattr(self, 'initial'):
            value = self.initial
        return mark_safe('<span %s>%s</span>' % (flatatt(final_attrs), value or ''))
    
    def _has_changed(self, initial, data):
        return False

class ReadOnlyField(forms.FileField):
    widget = ReadOnlyWidget
    def __init__(self, widget=None, label=None, initial=None, help_text=None):
        forms.Field.__init__(self, label=label, initial=initial, 
            help_text=help_text, widget=widget)
    
    def clean(self, value, initial=None):
        self.widget.initial = initial
        return initial

