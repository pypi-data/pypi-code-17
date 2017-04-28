from copy import deepcopy
from .async import async_wrapper
from .object import Object

def build_methods(obj, constants={}):
    """
    Binds Slack methods to an object.

    Method builder for adding many methods to an object at once.
    This should not be used for things that return other object types.

    For example, you should not use this with ``channels.history`` since
    that method should return a list of ``Message`` objects.

    Args:
        obj: The object to create methods on.
        constants (dict): A dictionary of constants to use
            when sending Slack API calls.
    """
    constants = deepcopy(constants)

    def gen_generic(method):
        async def new_method(**kwargs):
            nonlocal obj, constants, method
            to_return = await async_wrapper(
                obj._loop,
                obj._client.api_call,
                method,
                **constants,
                **kwargs
            )

            if to_return is not None:
                to_return = Object(to_return)

            return to_return
        return new_method
    
    for method in obj.methods:
        setattr(obj, method, gen_generic(obj.methods[method]))