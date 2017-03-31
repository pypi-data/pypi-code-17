from __future__ import unicode_literals

from wellaware._compat import add_metaclass
from wellaware.base import BaseAbstractEntity, BaseEntityMetaType, JsonProperty
from wellaware.resources.common import HttpError


@add_metaclass(BaseEntityMetaType)
class ReverseLookup(BaseAbstractEntity):

    tenant_uuid = JsonProperty("tenantUuid")  # type: str
    tenant_id = JsonProperty("tenantId")  # type: long
    entity_type = JsonProperty("type")  # type: str
    entity = JsonProperty("entity")  # type: dict

    def get_entity_as(self, entity_class):
        if entity_class and issubclass(entity_class, BaseAbstractEntity):
            return entity_class.from_dict(self.entity)
        return self.entity


@add_metaclass(BaseEntityMetaType)
class MultiReverseLookup(BaseAbstractEntity):

    lookups = JsonProperty("lookups")  # type: list(ReverseLookup)
    error_ids = JsonProperty("errorIds", klass=HttpError)  # type: dict(long, HttpError)


__all__ = ['ReverseLookup', 'MultiReverseLookup']
