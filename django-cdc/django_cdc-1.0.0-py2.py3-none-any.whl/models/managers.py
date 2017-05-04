from __future__ import unicode_literals

import logging

from django.db import models
import json
from django_cdc import settings as local_settings
from django_cdc.models.tracker import FieldInstanceTracker
from bitfield.types import BitHandler
from datetime import datetime,time
from django.db.models.fields.files import ImageFieldFile



from . import lambda_client


logger = logging.getLogger(__name__)

try:
    from django.utils.timezone import now as datetime_now
    assert datetime_now
except ImportError:
    import datetime
    datetime_now = datetime.datetime.now

models.signals.post_update = models.signals.Signal()
models.signals.bulk_create= models.signals.Signal()

class PythonObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,ImageFieldFile) or isinstance(obj,datetime) \
                or isinstance(obj,time) or isinstance(obj,BitHandler):
           return str(obj)
        return json.JSONEncoder.default(self, obj)

class DjangoCDCQuerySet(models.query.QuerySet):

    def update(self, **kwargs):
        super(DjangoCDCQuerySet, self).update(**kwargs)
        models.signals.post_update.send(sender=self.model,queryset=self,updates=kwargs)

    def bulk_create(self, objs, batch_size=None):
        super(DjangoCDCQuerySet, self).bulk_create(objs)
        models.signals.bulk_create.send(sender=self.model, queryset=self)

class DjangoCDCManager(models.Manager):

    def __init__(self, model, attname, exclude=[], foreign_keys=[], instance=None):
        super(DjangoCDCManager, self).__init__()
        self.model = model
        self.instance = instance
        self.attname = attname
        self._exclude = exclude
        self.foreign_keys = foreign_keys
        # set a hidden attribute on the  instance to control wether
        # we should track changes
        if instance is not None and not hasattr(
                instance, '__is_%s_enabled' % attname):
            setattr(instance, '__is_%s_enabled' % attname, True)
            #FieldTracker().contribute_to_class(instance, 'tracker')

    def enable_tracking(self):
        if self.instance is None:
            raise ValueError("Tracking can only be enabled or disabled "
                             "per model instance, not on a model class")
        setattr(self.instance, '__is_%s_enabled' % self.attname, True)
        #FieldTracker().contribute_to_class(self.instance, 'tracker')

    def disable_tracking(self):
        if self.instance is None:
            raise ValueError("Tracking can only be enabled or disabled "
                             "per model instance, not on a model class")
        setattr(self.instance, '__is_%s_enabled' % self.attname, False)

    def is_tracking_enabled(self):
        if local_settings.DISABLE_DJANGO_CDC:
            return False
        if self.instance is None:
            raise ValueError("Tracking can only be enabled or disabled "
                             "per model instance, not on a model class")
        return getattr(self.instance, '__is_%s_enabled' % self.attname)

    def get_queryset(self):
        return DjangoCDCQuerySet(self.model,using=self.db)

    def create_data_entry(self, instance,action_type,updates=None,
                        *args, **kwargs):
        myList = []
        name = ""
        if isinstance(instance, list):
            for var in instance:
                name = var._meta.db_table
                if getattr(var, self.attname).is_tracking_enabled():
                    data_entry = self.__get_data_entry(var,
                                                      action_type,
                                                      self._exclude,
                                                      self.foreign_keys,
                                                      updates)
                    if data_entry:
                        myList.append(data_entry)
                else:
                    logger.info("Tracking is disabled")
        else:
            if getattr(instance,self.attname).is_tracking_enabled():
                name = instance._meta.db_table
                data_entry = self.__get_data_entry(instance,
                                                  action_type,
                                                  self._exclude,
                                                  self.foreign_keys,
                                                  updates)
                if data_entry:
                    myList.append(data_entry)
            else:
                logger.info("Tracking is disabled")
        if myList:
            self.put_data_entry(name, *myList)


    def put_data_entry(self,name,*args, **kwargs):
        payload_json = json.dumps(args, cls=PythonObjectEncoder)
        table_name=name
        logger.info("My Data :%s", payload_json)
        try:
            function_name = local_settings.LAMBDA_FUNCTION_PREFIX + \
                            "-" + table_name

            lambda_client.invoke(FunctionName=function_name,
                                 InvocationType='Event', Payload=payload_json)
        except Exception as e:
            logger.error(
                "Error Occurred while invoking lambda function %s" % str(e))

    def __get_data_entry(self, instance, action_type, exclude, foreign_keys,updates):
        is_field_changed = True
        changed_fields = []
        attrs = {}
        if not updates and action_type == 'U':
            changed_fields = self.__get_changed_fields(instance, exclude)
            if not changed_fields:
                is_field_changed = False
            else:
                attrs["changed_fields"] = changed_fields
        elif updates:
            attrs["changed_fields"] = list(updates)

        if is_field_changed:
            prefix_for_foreign_key = "__"
            for field in instance._meta.fields:
                if field.name in foreign_keys.keys():
                    data = foreign_keys[field.name]
                    foreign_key_instance = getattr(instance, field.name)
                    attr_key = "{0}{1}".format(field.name,
                                               prefix_for_foreign_key)
                    if isinstance(data, list):
                        for val in data:
                            attrs[attr_key + val] = getattr(
                                foreign_key_instance, val)
                    else:
                        attrs[attr_key + data] = getattr(
                            foreign_key_instance, data)
                if field.attname not in exclude:
                    name = field.name \
                            if field.get_internal_type() == 'ForeignKey' \
                            else field.attname
                    attrs[name] = getattr(instance,
                                          field.attname)
            attrs["user_action"] = action_type

        else:
            logger.info("No field updated...exit!!")
        return attrs

            # manager.create(action_type = action_type, **attrs)

    def __get_changed_fields(self, instance, exclude, *args, **kwargs):
        fields = []
        if hasattr(instance, 'tracker'):
            for field in instance._meta.fields:
                if field.attname not in exclude and instance.tracker.has_changed(field.attname):
                    name = field.name if field.get_internal_type() == 'ForeignKey' \
                        else field.attname
                    fields.append(name)
        return fields


class DjangoCDCDescriptor(object):
    def __init__(self, model, manager_class, attname,exclude=[],
                 foreign_keys=[]):
        self.model = model
        self.manager_class = manager_class
        self.attname = attname
        self._exclude=exclude
        self.foreign_keys = foreign_keys

    def __get__(self, instance, owner):
        if instance is None:
            return self.manager_class(self.model, self.attname)
        return self.manager_class(self.model, self.attname,
                                  self._exclude, self.foreign_keys, instance)



class DjangoCDC(object):
    manager_class = DjangoCDCManager
    tracker_class = FieldInstanceTracker

    def __init__(self, exclude=[], foreign_keys={}):
        self._exclude = exclude
        self.foreign_keys = foreign_keys

    def contribute_to_class(self, cls, name):
        self.manager_class(cls, name, self._exclude,
                           self.foreign_keys
                          ).contribute_to_class(cls, 'objects')
        self.manager_name = name
        models.signals.class_prepared.connect(self.finalize, sender=cls)

    def initialize_tracker(self, sender, instance, **kwargs):
        if not isinstance(instance, self.model_class):
            return  # Only init instances of given model (including children)
        tracker = self.tracker_class(instance, self.fields, self.field_map)
        setattr(instance, "tracker", tracker)
        tracker.set_saved_fields()
        self.patch_save(instance)

    def patch_save(self, instance):
        original_save = instance.save
        def save(**kwargs):
            ret = original_save(**kwargs)
            update_fields = kwargs.get('update_fields')
            if not update_fields and update_fields is not None:  # () or []
                fields = update_fields
            elif update_fields is None:
                fields = None
            else:
                fields = (
                    field for field in update_fields if
                    field in self.fields
                )
            getattr(instance,"tracker").set_saved_fields(
                fields=fields
            )
            return ret
        instance.save = save

    def bulk_create(self,queryset,*args,**kwargs):
        if queryset:
            manager = getattr(queryset[0], self.manager_name)
            manager.create_data_entry(list(queryset),'I')

    def post_update(self, queryset,updates, *args, **kwargs):
        #FIELD_TRACKER NOT WORKING
        if queryset:
            manager = getattr(queryset[0], self.manager_name)
            manager.create_data_entry(list(queryset),'U',updates)

    def post_save(self, instance, created, **kwargs):
        # ignore if it is disabled
        #if getattr(instance, self.manager_name).is_tracking_enabled():
        manager = getattr(instance, self.manager_name)
        manager.create_data_entry(instance, created and 'I' or 'U')

    def post_delete(self, instance, **kwargs):
        # ignore if it is disabled
        #if getattr(instance, self.manager_name).is_tracking_enabled():
        manager = getattr(instance, self.manager_name)
        manager.create_data_entry(instance, 'D')

    def get_field_map(self, cls):
        """Returns dict mapping fields names to model attribute names"""
        field_map = dict((field, field) for field in self.fields)
        all_fields = dict((f.name, f.attname) for f in cls._meta.fields)
        field_map.update(**dict((k, v) for (k, v) in all_fields.items()
                                if k in field_map))
        return field_map

    def finalize(self, sender, **kwargs):
        #log_entry_model = self.create_data_entry_model(sender)
        #prev_instance=models.signals.pre_save.connect(self.pre_save,sender=sender,weak=False)

        # For Field tracking
        self.fields = (field.attname for field in sender._meta.fields)
        self.fields = set(self.fields)
        self.field_map = self.get_field_map(sender)
        models.signals.post_init.connect(self.initialize_tracker)
        self.model_class = sender
        setattr(sender,"tracker", self)

        models.signals.bulk_create.connect(
            self.bulk_create,sender=sender,weak=False)
        models.signals.post_update.connect(
            self.post_update, sender=sender, weak=False)
        models.signals.post_save.connect(
            self.post_save, sender=sender, weak=False)
        models.signals.post_delete.connect(
            self.post_delete, sender=sender, weak=False)
        descriptor = DjangoCDCDescriptor(
            sender, self.manager_class, self.manager_name,
            self._exclude,self.foreign_keys)
        setattr(sender, self.manager_name, descriptor)
