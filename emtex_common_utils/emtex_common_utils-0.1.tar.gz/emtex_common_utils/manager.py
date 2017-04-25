import datetime

from django.db import models


class BaseQuerySet(models.query.QuerySet):
    def update(self, **kwargs):
        kwargs['modified_date'] = datetime.datetime.now()
        return super(BaseQuerySet, self).update(**kwargs)


class BaseManager(models.Manager):
    """
    Base Model Manager. Other managers extend this
    """

    def get_queryset(self):
        """
        Override base QuerySet to show only enabled items
        """
        return BaseQuerySet(self.model, using=self._db).filter(is_active=True)

