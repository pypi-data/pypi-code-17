import json

import datetime
from restkit import Resource

import runscope


class RunScopeResource(Resource):
    collection_class = None
    resource_path = None
    resource_method = None

    def __init__(self, parent, config=None, data=None,**kwargs):
        search_url = "https://api.runscope.com"
        super(RunScopeResource, self).__init__(search_url, follow_redirect=True,
                                               max_follow_redirect=10, **kwargs)

        self.defaults = {
            'headers': {
                'Authorization': "Bearer " + runscope.get_defaults()['access_token']
            }
        }

        self._config = config
        self._data = data
        self._parent = parent

    def __getattr__(self, item):
        return self.data[item]

    def request(self, method, path=None, payload=None, headers=None, params_dict=None, **params):

        if headers is not None:
            headers.update(self.defaults['headers'])
        else:
            headers = self.defaults['headers']

        resp = super(RunScopeResource, self).request(method, path, payload, headers, params_dict, **params)
        return json.loads(resp.body_string())

    def build_parent_ids(self, attributes=None):
        if attributes is None:
            attributes = {}

        if self._id_key is not None:
            id_key = self._resource_type+"_id"
            attributes[id_key] = self._data[self._id_key]
        if self._parent is not None:
            self._parent.build_parent_ids(attributes)
        return attributes

    @property
    def data(self):
        if self._data is None:
            self.fetch()
        return self._data

    @property
    def resource_path(self):
        if 'path_pattern' not in self._config:
            raise RuntimeError("Could not find 'path_pattern' in {config} for {name}".format(
                config=self._config,
                name=self.__class__.__name__
            ))
        resource_path = self._config['path_pattern']
        if any(bracket in resource_path for bracket in ['{','}']):
            format_variables = self._parent.data.copy()
            format_variables.update(self.build_parent_ids())

            resource_path = resource_path.format(**format_variables)

        return resource_path

    def fetch(self):
        raw_response = self.get(self.resource_path)
        self._data = raw_response['data']

    def _cast_to_datetime(self, value):
        return datetime.datetime.fromtimestamp(value)


    def keys(self):
        """
        Implemented to allow casting to a `dict`
        :return:
        """
        return self._data.keys()

    def __getitem__(self, key):
        """
        Implemented to allow casting to a `dict`
        :return:
        """
        if hasattr(self, key):
            return getattr(self, key)
        return self._data[key]


class RunScopeResourceCollection(RunScopeResource):
    _resource_class = None

    def __init__(self, parent, resource_class, config=None, **kwargs):
        super(RunScopeResourceCollection, self).__init__(config=config, parent=parent,**kwargs)
        self._parent = parent
        self._resource_class = resource_class

    def filter(self, **filter_args):
        for datum in self.data:
            yield self._resource_class(
                data=datum,
                parent=self
            )

    def all(self):
        for datum in self.data:
            yield self._resource_class(
                data=datum,
                parent=self
            )

    def build_parent_ids(self, attributes=None):
        if attributes is None:
            attributes = {}
        self._parent.build_parent_ids(attributes)
        return attributes
