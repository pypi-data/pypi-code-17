from datetime import datetime

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class TrashableModelMixin(models.Model):
    """
    Allows a model to be sent to trash.
    """
    trashed_at = models.DateTimeField(null=True, blank=True,
                                      help_text=_('If set, this object is considered to be in the'
                                                  ' trash can.'))

    class Meta:
        abstract = True

    class Filters:
        """
        Convenience filters that can be used when querying this model.
        """
        AVAILABLE = Q(trashed_at=None)
        TRASHED = Q(trashed_at__isnull=False)

    def is_trashed(self):
        """
        :return: True if this model instance is in the trash.
        """
        return bool(self.trashed_at)
    is_trashed.short_description = _('In trash')
    is_trashed.boolean = True

    def trash(self):
        """
        Marks this model instance as trashed.
        """
        self.trashed_at = datetime.now()
        self.save()

    def restore(self):
        """
        Removes this model from trash.
        """
        self.trashed_at = None
        self.save()
