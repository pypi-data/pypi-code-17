from __future__ import unicode_literals

from wellaware._compat import add_metaclass
from wellaware.base import BaseAbstractEntity, BaseEntityMetaType, JsonProperty


@add_metaclass(BaseEntityMetaType)
class RollupUpdateResponse(BaseAbstractEntity):
    """
    Represents a Rollup Update Response.
    """

    rollup_updates = JsonProperty('rollupUpdates')
    errors = JsonProperty('errors')


@add_metaclass(BaseEntityMetaType)
class DataSaveResponse(BaseAbstractEntity):
    """
    Represents a Data Create Response.
    """

    errors = JsonProperty('errors')


@add_metaclass(BaseEntityMetaType)
class DataRetrieveResponse(BaseAbstractEntity):
    """
    Represents a Data Retrieve Response.
    """

    observations = JsonProperty('observations')
    errors = JsonProperty('errors')


@add_metaclass(BaseEntityMetaType)
class DataModificationResponse(BaseAbstractEntity):
    """
    Represents a Data Update Response.
    """

    errors = JsonProperty('errors')


__all__ = ['DataSaveResponse', 'DataModificationResponse', 'DataRetrieveResponse', 'RollupUpdateResponse']


