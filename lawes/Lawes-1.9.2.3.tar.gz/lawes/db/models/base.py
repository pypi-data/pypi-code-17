# -*- coding:utf-8 -*-

from lawes.db.models.query import QuerySet
from lawes.utils import six
from lawes.db.models.options import Options

class ModelBase(type):

    def __new__(cls, name, bases, attrs):
        """  changed Field to true type
        """
        super_new = super(ModelBase, cls).__new__
        # if it is not the ModelBase , return
        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class.
        # new_class = super_new(cls, name, bases, attrs)
        # module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, attrs)
        meta = attrs.pop('Meta', None)
        if not meta:
            meta = getattr(new_class, 'Meta', None)
        # db_table is the collection name in mongodb
        db_table = new_class.__module__.split('.')[-1] + '_' + new_class.__name__.lower()
        kwargs = {"db_table": db_table}
        new_class._meta = Options(meta, **kwargs)

        # set the local_fields at Options: {'name': lawes.db.models.fields.CharField}
        for obj_name, obj in attrs.items():
            if hasattr(obj, 'contribute_to_class'):
                new_class._meta.add_field(obj_name=obj_name, obj=obj)

        # create the objects
        new_class.objects = QuerySet(model=new_class)

        return new_class


class Model(six.with_metaclass(ModelBase)):

    pk_attname = '_id'
    save_fields = []


    def __init__(self, *args, **kwargs):
        # set the real value to the model
        for obj_name in self._meta.local_fields:
            obj = self._meta.local_fields[obj_name]
            setattr(self, obj_name, obj.value)

        # creat the index and unique in db
        # self.objects.init_index(db_indexs = self._meta.db_indexs)

        super(Model, self).__init__()


    def __setattr__(self, key, value):
        super(Model, self).__setattr__(key, value)
        if hasattr(self, '_id'):
            self.save_fields.append(key)


    def save(self):
        self._save_table()


    def _save_table(self):

        pk_val = self._get_pk_val()
        # pk_set is true for updating, pk_set is true for inserting
        pk_set = pk_val is not None
        data = self.to_dict(fields='save_fields') if pk_set else self.to_dict()
        # the format must be correct
        checking_keys = set(self._meta.local_fields) & set(data)
        for key in checking_keys:
            self._meta.local_fields[key].check_type(value=data[key])
        if pk_set:
            self._do_update(data=data)
        else:
            result = self._do_insert(data=data)
            setattr(self, self.pk_attname, result)


    def _get_pk_val(self):
        """ get _id: None: INSERT; not None: UPDATE
        """
        if not hasattr(self, self.pk_attname):
            return None
        else:
            return getattr(self, self.pk_attname)


    @classmethod
    def _do_insert(cls, data):
        """ 向 mongodb 插入数据
        """
        return cls.objects._insert(data=data)


    @classmethod
    def _do_update(cls, data):
        """ doing update in mongodb
        """
        return cls.objects._update(data=data)


    def to_dict(self, fields=''):
        """ if the values of the fields is 'save_fields' , only change the fields parts
        """
        if fields == 'save_fields':
            fields_type = self.save_fields
        else:
            fields_type = self._meta.local_fields
        result = {}

        for field in fields_type:
            if hasattr(self, field):
                value = getattr(self, field)
                result[field] = value

        if hasattr(self, '_id'):
            result['_id'] = self._id

        return result


    def to_obj(self, data={}):

        for field in data:
            setattr(self, field, data[field])
        for field in self._meta.local_fields:
            if field in data:
                value = data[field]
            else:
                value = self._meta.local_fields[field].value
            setattr(self, field, value)
        if '_id' in data:
            self._id = data['_id']
        return self


    def delete(self):
        return self.objects._remove(_id=self._id)
