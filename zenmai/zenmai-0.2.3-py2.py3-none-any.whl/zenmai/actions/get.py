from zenmai.decorators import with_context
from dictknife import Accessor


strict_default = object()


@with_context
def get(name, context, default=strict_default, accessor=Accessor()):
    try:
        if "#/" not in name:
            return getattr(context.scope, name)
        else:
            subname, path = name.split("#/", 2)
            root = getattr(context.scope, subname)
            return accessor.access(root, path.split("/"))
    except (AttributeError, KeyError):
        if default is strict_default:
            raise
        return default
