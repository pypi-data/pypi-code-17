import keyword


class Context(object):
    def __init__(self, module, loader, evaluator, filename=None):
        self.scope = Scope(module)
        self.accessor = Accessor(self)
        self.loader = loader
        self.evaluator = evaluator
        self.filename = filename

    def new_child(self, filename, scope=None):
        scope = scope or self.scope
        return self.__class__(scope, self.loader, self.evaluator, filename=filename)

    @property
    def rootscope(self):
        if hasattr(self.scope, "get_rootscope"):
            return self.scope.get_rootscope()
        else:
            return self.scope

    def assign(self, name, value):
        setattr(self.scope, name, value)


class Scope(object):
    def __init__(self, parent):
        self.parent = parent

    @classmethod
    def mergewith(cls, current, parent):
        scope = cls(cls(parent))
        scope.__dict__.update(current.__dict__)
        return scope

    def __getattr__(self, name):
        return getattr(self.parent, name)

    def get_rootscope(self):
        if self.parent is None:
            return self

        if hasattr(self.parent, "get_rootscope"):
            return self.parent.get_rootscope()
        else:
            return self.parent


class Accessor(object):
    def __init__(self, context):
        self.context = context

    def get_action(self, name):
        path = name.split(".")
        action = self.context.scope
        for p in path[:-1]:
            action = getattr(action, p)
        action = getattr(action, self.normalize_name(path[-1]))
        return action

    def get_additionals(self, method):
        additionals = getattr(method, "additionals", [])
        return [(name, getattr(self, name)) for name in additionals]

    def normalize_name(self, name):
        if keyword.iskeyword(name):
            return name + "_"
        else:
            return name
