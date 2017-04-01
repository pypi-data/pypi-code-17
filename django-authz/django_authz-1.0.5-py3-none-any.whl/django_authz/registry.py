class AuthzRegistry(object):

    def __init__(self):
        self._implementation_map = {}  # {name:implementation}

    def __str__(self):
        return "Role Registry"

    def register(self, role_implementation_class):
        #print("registry.register %s" % role_implementation_class)

        instance = role_implementation_class()
        role_name = instance.name

        if role_name in list(self._implementation_map.keys()):
            print(("Warning: role %s already in registry with implementation: %s" %
                   (role_name, self._implementation_map[role_name])))
        self._implementation_map[role_name] = instance

    def get_implementation(self, role_name):
        return self._implementation_map.get(role_name, None)
    get = get_implementation

    def __iter__(self):
        for name, implementation in list(self._implementation_map.items()):
            yield (name, implementation)

authz_registry = AuthzRegistry()
