
from lawes.utils.encoding import python_2_unicode_compatible
from lawes.db.models.fields import Field

@python_2_unicode_compatible
class Options(object):
    """ for the model to set default
    """
    def __init__(self, meta, app_label=None):
        self.meta = meta
        self.app_label = app_label
        self.local_fields = {} # {'name': lawes.db.models.fields.CharField }
        self.db_indexs = {}

    def add_field(self, obj_name, obj):
        self.local_fields[obj_name] = obj
        if isinstance(obj, Field):
            if obj.db_index is True or obj.unique is True:
                self.db_indexs[obj_name] = { 'unique': obj.unique }
