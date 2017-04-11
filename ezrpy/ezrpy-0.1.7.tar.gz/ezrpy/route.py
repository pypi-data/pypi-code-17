class RouteFactory(object):
    def __init__(self, base_route):
        self.base_route = self._clean_base(base_route)

        self.list_format = "%s/"
        self.post_format = "%s/"
        self.get_format = "%s/<pk>/"
        self.delete_format = "%s/<pk>/"
        self.put_format = "%s/<pk>/"

    def create_list(self, instance):
        return self.create_route(self.list_format % instance.get_name())

    def create_post(self, instance):
        return self.create_route(self.post_format % instance.get_name())

    def create_get(self, instance):
        return self.create_route(self.get_format % instance.get_name())

    def create_delete(self, instance):
        return self.create_route(self.delete_format % instance.get_name())

    def create_put(self, instance):
        return self.create_route(self.put_format % instance.get_name())

    def create_route(self, relative):
        return '/' + self.base_route + '/' + relative

    def _clean_base(self, base):
        if base.startswith('/'):
            base = base[1:]

        if base.endswith('/'):
            base = base[:-1]

        return base

    def clean_relative_route(self, route):
        if route.startswith('/'):
            route = route[1:]

        if not route.endswith('/'):
            route += '/'

        return route
