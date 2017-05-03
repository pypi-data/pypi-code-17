from collections import ChainMap
from zenmai.decorators import with_context


@with_context
def partial(fnname, context, **kwargs):
    accessor = context.accessor
    action = accessor.get_action(fnname[1:])

    def _partial(d, *args, **new_kwargs):
        return action(d, *args, **ChainMap(new_kwargs, kwargs))

    _partial.additionals = [name for name, _ in accessor.get_additionals(action)]
    return _partial
