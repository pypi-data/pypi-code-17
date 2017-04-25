from datetime import datetime

import django.db.models.options as options
from django.db import models

from middleware import get_current_user
from .manager import BaseManager

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('log_fields', 'log_model_name',)


class BaseModel(models.Model):
    """
    An abstract base class model that provides self-updating
    `created_date`,  `modified_date`, `created_by`, `modified_by` fields.

    I am not using django magic of `auto_now` and `auto_now_add`.
    Reason:
        1: http://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add
        2: https://code.djangoproject.com/ticket/22995
    """

    created_date = models.DateTimeField(editable=False)
    modified_date = models.DateTimeField()
    created_by = models.CharField(max_length=50, blank=True, null=True, default='')
    modified_by = models.CharField(max_length=50, blank=True, null=True, default='')
    is_active = models.BooleanField(default=True)

    # This will filter out is_active = False
    objects = BaseManager()

    # This will return all rows
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = datetime.now()
        self.modified_date = datetime.now()
        self.log_changes()
        return super(BaseModel, self).save(*args, **kwargs)

    def log_changes(self):
        try:
            fields = self._meta.log_fields
            model_name = self._meta.log_model_name
        except AttributeError:
            pass
        else:
            for field in fields:
                old_value = self.old_values.get(field)
                new_value = getattr(self, field)
                if old_value != new_value:
                    model_name.objects.create(
                        object_id=self.id,
                        column_name=field,
                        column_old_value=old_value,
                        column_new_value=new_value,
                        modified_by=get_current_user(),
                        created_by=get_current_user(),
                    )
                    self.old_values[field] = new_value


class BaseLogModel(BaseModel):
    """
    Base model to track changes in any model
    """
    object_id = models.CharField(max_length=11)
    column_name = models.CharField(max_length=255)
    column_old_value = models.CharField(max_length=255)
    column_new_value = models.CharField(max_length=255)

    class Meta:
        abstract = True

