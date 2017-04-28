import asyncio
from concurrent.futures import ThreadPoolExecutor

async def async_wrapper(loop, *args, **kwargs):
    """
    Executes a function asynchronously.

    Args:
        *args:
            A variadic list of arguments. The first argument should
            be the function to execute. All other arguments should be
            arguments for the function.
        **kwargs:
            Keyed arguments to pass to the function when executing.
    """
    fn = args[0]
    real_args = args[1:]
    return await loop.run_in_executor(ThreadPoolExecutor(), lambda: fn(*real_args, **kwargs))