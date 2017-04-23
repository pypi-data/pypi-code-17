from django.db import models
from boogie.manager import QuerySetManager


class ModelWithQsManager(models.Model):
    name = models.CharField(max_length=100)
    objects = QuerySetManager()

    def __str__(self):
        return self.name

