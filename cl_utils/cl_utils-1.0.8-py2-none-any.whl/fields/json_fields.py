''' Retrieved from http://www.davidcramer.net/code/448/cleaning-up-with-json-and-sql.html '''

import json

from django.db import models
from django import forms


class JSONWidget(forms.Textarea):
    def render(self, name, value, attrs=None):
        if not isinstance(value, basestring):
            value = json.dumps(value, indent=2)
        return super(JSONWidget, self).render(name, value, attrs)

class JSONFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = JSONWidget
        super(JSONFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value:
            return
        try:
            return json.loads(value)
        except Exception, exc:
            raise forms.ValidationError(u'JSON decode error: %s' % (unicode(exc),))

class JSONField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def formfield(self, **kwargs):
        return super(JSONField, self).formfield(form_class=JSONFormField, **kwargs)

    def to_python(self, value):
        if isinstance(value, basestring):
            if value == '':
                value = '{}'
            value = json.loads(value)
        return value

    def get_db_prep_save(self, value, *args, **kwargs):
        if value is None:
            return
        else:
            value = json.dumps(value)
            return super(JSONField, self).get_db_prep_save(value, *args, **kwargs)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_db_prep_value(value)

    def south_field_triple(self):
        'Returns a suitable description of this field for South.'
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        fc = self.__class__
        field_class = '%s.%s' % (fc.__module__, fc.__name__)
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
