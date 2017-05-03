from dictknife import Accessor
from zenmai.decorators import with_context
from .dynamic import get_locals


strict_default = object()


class EvalVariableError(Exception):
    pass


@with_context
def get(name, context, default=strict_default, accessor=Accessor()):
    try:
        if "#/" not in name:
            return getattr(context.scope, name)
        else:
            subname, path = name.split("#/", 2)
            root = getattr(context.scope, subname)
            return accessor.access(root, path.split("/"))
    except AttributeError as e:
        if default is strict_default:
            vs = sorted(k for k in get_locals(context.scope).keys() if not k.startswith("__"))
            msg = "{e}\n accessible variables: {vs}".format(e=e, vs=vs)
            raise EvalVariableError(msg)
        return default
    except KeyError as e:
        if default is strict_default:
            raise EvalVariableError("KeyError: {}".format(name))
        return default
