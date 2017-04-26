import django
from django.db.models import Manager

from .query import MessageQuerySet

if django.VERSION < (1, 7):
    class MessageManager(Manager):
        """Message manager"""
        def get_queryset(self):
            return MessageQuerySet(self.model, using=self._db)

        if django.VERSION < (1, 6):
            get_query_set = get_queryset

        def undelivered(self, to=None):
            """Fetch only undelivered messages"""
            return self.get_queryset().undelivered(to)
else:
    class MessageManager(Manager.from_queryset(MessageQuerySet)):
        """Message manager"""
        pass
