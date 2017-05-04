"""Standard Cortical Observer - Model Repository

The SCO Model Repository is a registry for computational models that predict
brain responses to arbitrary sensory inputs.

Each model in the registry defines the set of expected input parameters and the
set of outputs that are produced.

The default implementation of the model registry uses MongoDB as storeage
backend.
"""

import datetime

from scodata.attribute import AttributeDefinition
from scodata.datastore import MongoDBStore, ObjectHandle


class ModelHandle(ObjectHandle):
    """Handle for registered model in repository.

    Attributes
    ----------
    identifier : string
        Unique model identifier
    properties : Dictionary
        Dictionary of model specific properties.
    parameters : list(scodata.attribute.AttributeDefinition)
        List of attribute definitions for model run parameters
    timestamp : datetime
        Time stamp of object creation (UTC time). If None, the current
        date and time is used.
    """
    def __init__(self, identifier, properties, parameters, timestamp=None):
        """Initialize the model handle attributes.

        Parameters
        ----------
        identifier : string
            Unique model identifier
        properties : Dictionary
            Dictionary of object specific properties.
        parameters : list(scodata.attribute.AttributeDefinition)
            List of attribute definitions for model run parameters
        timestamp : datetime, optional
            Time stamp of object creation (UTC time). If None, the current
            date and time is used.
        """
        super(ModelHandle, self).__init__(identifier, timestamp, properties)
        self.parameters = parameters

    @property
    def is_model(self):
        """Flag indicating that this object represents an model description.

        Returns
        -------
        Boolean
            True
        """
        return True


class DefaultModelRegistry(MongoDBStore):
    """Default implementation for model registry. Uses MongoDB as storage
    backend and makes use of the SCO datastore implementation. Provides
    wrappers for delete, exists, get, and list model operations.
    """
    def __init__(self, mongo_collection):
        """Initialize the MongoDB collection where models are being stored.

        Parameters
        ----------
        mongo_collection : Collection
            Collection in MongoDB
        """
        super(DefaultModelRegistry, self).__init__(mongo_collection)

    def delete_model(self, identifier, erase=False):
        """Delete the model with given identifier in the database. Returns the
        handle for the deleted model or None if object identifier is unknown.

        Parameters
        ----------
        identifier : string
            Unique model identifier
        erase : Boolean, optinal
            If true, the record will be deleted from the database. Otherwise,
            the active flag will be set to False to support provenance tracking.

        Returns
        -------
        ModelHandle
        """
        self.delete_object(identifier, erase=erase)

    def exists_model(self, identifier):
        """Returns true if a model with the given identifier exists in the
        registry.

        Parameters
        ----------
        identifier : string
            Unique model identifier

        Returns
        -------
        Boolean
            True, if model with given identifier exists.
        """
        # Return True if query for object identifier with active flag on returns
        # a result.
        return self.exists_object(identifier)

    def from_json(self, document):
        """Create a model database object from a given Json document.

        Parameters
        ----------
        document : JSON
            Json representation of the object

        Returns
        ModelHandle
        """
        # The timestamp is optional (e.g., in cases where model definitions are
        # loaded from file).
        if 'timestamp' in document:
            timestamp = datetime.datetime.strptime(
                document['timestamp'],
                '%Y-%m-%dT%H:%M:%S.%f'
            )
        else:
            timestamp = None
        # Create handle for database object
        return ModelHandle(
            document['_id'],
            document['properties'],
            [AttributeDefinition.from_json(el) for el in document['parameters']],
            timestamp=timestamp
        )

    def get_model(self, identifier):
        """Retrieve model with given identifier from the database.

        Parameters
        ----------
        identifier : string
            Unique model identifier

        Returns
        -------
        ModelHandle
            Handle for model with given identifier or None if no model
            with identifier exists.
        """
        return self.get_object(identifier, include_inactive=False)

    def list_models(self, limit=-1, offset=-1):
        """List models in the database. Takes optional parameters limit and
        offset for pagination.

        Parameters
        ----------
        limit : int
            Limit number of models in the result set
        offset : int
            Set offset in list (order as defined by object store)

        Returns
        -------
        ObjectListing
        """
        return self.list_objects(limit=limit, offset=offset)

    def register_model(self, identifier, properties, parameters):
        """Create an experiment object for the subject and image group. Objects
        are referenced by their identifier. The reference to a functional data
        object is optional.

        Raises ValueError if no valid experiment name is given in property list.

        Parameters
        ----------
        identifier : string
            Unique model identifier
        properties : Dictionary
            Dictionary of model specific properties.
        parameters : list(scodata.attribute.AttributeDefinition)
            List of attribute definitions for model run parameters

        Returns
        -------
        ModelHandle
            Handle for created model object in database
        """
        # Create object handle and store it in database before returning it
        obj = ModelHandle(identifier, properties, parameters)
        self.insert_object(obj)
        return obj

    def to_json(self, model):
        """Create a Json-like object for a model.

        Parameters
        ----------
        model : ModelHandle

        Returns
        -------
        dict
            Json-like object representation
        """
        # Get the basic Json object from the super class
        obj = super(DefaultModelRegistry, self).to_json(model)
        # Add model parameter
        obj['parameters'] = [
            para.to_json() for para in model.parameters
        ]
        return obj
