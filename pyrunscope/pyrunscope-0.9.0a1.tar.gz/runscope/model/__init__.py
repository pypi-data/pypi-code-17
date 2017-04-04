import json, pkg_resources


class _ApiDefinition(object):
    def __init__(self):
        self.definition = {}

    def load(self, item_name):
        self.definition[item_name] = json.loads(
            pkg_resources.resource_string('runscope', 'resources/api_description/{rsc_name}.json'.format(rsc_name=item_name))
        )
        self.definition[item_name]['_name'] = item_name

    def __getattr__(self, item):
        if item not in self.definition:
            self.load(item)
        return self.definition[item]

    def _load_resource(self, resource_name):
        return getattr(self, resource_name)


if __name__ == 'runscope.model':
    apidefinition = _ApiDefinition()
