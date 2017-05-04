import datetime

from django.db.models import DateTimeField

class CreationDateTimeField(DateTimeField):
    """
      CreationDateTimeField

      By default, sets editable=False, blank=True, default=datetime.now
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('default', datetime.datetime.now)
        DateTimeField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "DateTimeField"

    def south_field_triple(self):
        'Returns a suitable description of this field for South.'
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        fc = self.__class__
        field_class = '%s.%s' % (fc.__module__, fc.__name__)
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)

class ModificationDateTimeField(CreationDateTimeField):
    """
      ModificationDateTimeField

      By default, sets editable=False, blank=True, default=datetime.now

      Sets value to datetime.now() on each save of the model.
    """

    def pre_save(self, model, add):
        value = datetime.datetime.now()
        setattr(model, self.attname, value)
        return value

    def get_internal_type(self):
        return "DateTimeField"

