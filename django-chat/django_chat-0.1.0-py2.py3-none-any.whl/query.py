"""Message related query sets"""
from django.db.models.query import QuerySet


class MessageQuerySet(QuerySet):
    """Message query set"""

    def undelivered(self, to=None):
        """Fetch only undelivered messages"""
        if to is not None:
            return self.filter(deliveries__receiver=to,
                               deliveries__delivered_at__isnull=True)
        else:
            return self.filter(deliveries__delivered_at__isnull=True)
