import keyword


class Context(object):
    def __init__(self, module, loader, evaluator, filename=None):
        self.scope = Scope(module)
        self.accessor = Accessor(self)
        self.loader = loader
        self.evaluator = evaluator
        self.filename = filename

    def new_child(self, filename):
        return self.__class__(self.scope, self.loader, self.evaluator, filename=filename)

    def assign(self, name, value):
        setattr(self.scope, name, value)


class Scope(object):
    def __init__(self, parent):
        self.parent = parent

    def __getattr__(self, name):
        return getattr(self.parent, name)


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
