from django.db.models import Model as DjModel
from .manager import QuerySetManager


class Model(DjModel):
    """
    Base Boogie model class.
    """

    class Meta:
        abstract = True

    objects = QuerySetManager()