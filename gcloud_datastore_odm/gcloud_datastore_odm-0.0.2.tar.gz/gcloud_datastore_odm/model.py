# -*- coding: utf-8 -*-
"""
    model

    :license: see LICENSE for details.
"""
from datetime import datetime

from schematics.models import Model as BaseModel
from google.cloud.datastore.entity import Entity

from .types import DateTimeType
from .datastore_client import datastore_client


class Model(BaseModel):
    _index_fields = []

    created_at = DateTimeType()
    updated_at = DateTimeType()
    ignore_rogue_fields = False

    @property
    def _non_indexed(self):
        return list(set(self._fields.keys()) - set(self._index_fields))

    def __init__(self, *args, **kwargs):
        id = kwargs.pop('id', None)
        if id:
            key = datastore_client.key(self.__class__.__name__, id)
        else:
            key = datastore_client.key(self.__class__.__name__)

        entity = kwargs.pop('entity', None)
        if entity:
            assert entity.key.kind == self.__class__.__name__, (
                "Expected entity of kind '%s', found '%s' instead." % (
                    self.__class__.__name__, entity.key.kind
                )
            )
        if id:
            # Only fetch entity when id is there
            entity = datastore_client.get(key)

        if entity is None:
            self._entity = Entity(key, exclude_from_indexes=self._non_indexed)
        else:
            self._entity = entity
            if self.ignore_rogue_fields:
                raw_data = {}
                for k, v in entity.items():
                    if k in self._fields.keys():
                        raw_data[k] = v
            else:
                raw_data = dict(entity.items())
            kwargs['raw_data'] = raw_data

        # Remove rawdata from args if available
        if len(args):
            args = args[1:]

        super(Model, self).__init__(*args, **kwargs)

    @property
    def id(self):
        "Returns datastore id for this entity"
        if self._entity:
            return self._entity.key.id_or_name

    @property
    def datastore_key(self):
        "Returns datastore key for this entity"
        if self._entity:
            return self._entity.key

    @classmethod
    def get_by_id(cls, id):
        key = datastore_client.key(cls.__name__, id)
        entity = datastore_client.get(key)
        if entity:
            return cls(entity=entity)

    @classmethod
    def query(cls):
        return datastore_client.query(kind=cls.__name__)

    def save(self):
        if not self.created_at:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.validate()
        self._entity.update(self.to_primitive())
        datastore_client.put(self._entity)
