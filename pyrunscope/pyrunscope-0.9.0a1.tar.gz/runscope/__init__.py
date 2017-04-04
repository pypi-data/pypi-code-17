import os

from runscope.admin import Admin
import importlib

from runscope.model import apidefinition
from runscope.model.resource import RunScopeResource, RunScopeResourceCollection

DEFAULTS = {}


def client(module_name):
    return _build_class(module_name)(parent=None)


def _build_class(name):
    class_methods = _build_class_attributes(name)
    bases = [RunScopeResource]
    cls = type(str("model." + name.capitalize()), tuple(bases), class_methods)
    return cls


def _build_collection_class(name, resource_model):
    class_methods = {}
    _build_metadata_attributes(class_methods, resource_model)
    class_methods['_is_collection'] = True

    bases = [RunScopeResourceCollection]
    cls = type(str("model.collection." + name.capitalize()), tuple(bases), class_methods)
    return cls


def _build_class_attributes(resource_name):
    resource_model = apidefinition._load_resource(resource_name)
    attrs = {}

    if 'has_many' in resource_model:
        _build_collection_attributes(attrs, resource_model['has_many'])

    if 'fields' in resource_model:
        _build_field_getters(attrs, resource_model['fields'])

    _build_metadata_attributes(attrs, resource_model)
    attrs['_is_collection'] = False

    return attrs


def _build_field_getters(attributes, fields_model):
    for field in fields_model:
        attributes[field['name']] = _build_field_getter(field)


def _build_field_getter(field_model):
    field_name = field_model['name']
    field_type = field_model['type']
    method_name = "_cast_to_" + field_type

    return property(lambda self: getattr(self, method_name)(self._data[field_name]))


def _build_metadata_attributes(attributes, resource_model):
    if '_id_key' not in resource_model:
        raise RuntimeError("Could not find '_id_key' in {resource_model}".format(
            resource_model=resource_model
        ))

    attributes['_id_key'] = resource_model['_id_key']

    if 'path_pattern' not in resource_model:
        raise RuntimeError("Could not find 'path_pattern' in {resource_model}".format(
            resource_model=resource_model
        ))
    attributes['path_pattern'] = resource_model['path_pattern']
    name_key = 'name' if 'name' in resource_model else '_name'
    attributes['_resource_type'] = resource_model[name_key]


def _build_collection_attributes(attributes, collections):
    for collection in collections:
        attributes[collection['name']] = _build_collection_attr(collection['name'], collection)
    return attributes


def _build_collection_attr(name, config):
    cls = _build_collection_class(name, config)

    def _get_collection(self):
        resource_cls = _build_class(config['resource'])
        return cls(resource_class=resource_cls, config=config, parent=self)

    _get_collection.__name__ = str(name.lower())

    return property(_get_collection)


def set_defaults(**kwargs):
    global DEFAULTS
    DEFAULTS.update(kwargs)


def get_defaults():
    global DEFAULTS
    return DEFAULTS


if __name__ == 'runscope':
    # If environment variables have been provided, use them
    if 'RS_ACCESS_TOKEN' in os.environ:
        set_defaults(
            access_token=os.environ['RS_ACCESS_TOKEN']
        )
