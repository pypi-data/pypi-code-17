
from lawes.utils.encoding import python_2_unicode_compatible
from lawes.db.models.fields import Field

DEFAULT_NAMES = ('verbose_name', 'verbose_name_plural', 'db_table', 'ordering',
                 'unique_together', 'permissions', 'get_latest_by',
                 'order_with_respect_to', 'app_label', 'db_tablespace',
                 'abstract', 'managed', 'proxy', 'swappable', 'auto_created',
                 'index_together', 'apps', 'default_permissions',
                 'select_on_save', 'default_related_name')

@python_2_unicode_compatible
class Options(object):
    """ for the model to set default
    """
    def __init__(self, meta, db_table=None):

        self.db_table = db_table
        self.local_fields = {} # {'name': lawes.db.models.fields.CharField }
        self.db_indexs = {}
        self.meta = meta
        # set attribute for Option from Model's Meta
        if meta:
            meta_attrs = self.meta.__dict__.copy()
        else:
            meta_attrs = {}
        for attr_name in meta_attrs:
            if attr_name.startswith('_'):
                continue
            if attr_name in DEFAULT_NAMES:
                setattr(self, attr_name, meta_attrs[attr_name])

    def add_field(self, obj_name, obj):
        self.local_fields[obj_name] = obj
        if isinstance(obj, Field):
            if obj.db_index is True or obj.unique is True:
                self.db_indexs[obj_name] = { 'unique': obj.unique }


    def __str__(self):
        return ''
