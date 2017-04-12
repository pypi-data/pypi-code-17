from concurrent.futures import ThreadPoolExecutor

_pool = None


def get_pool(pool_size=4):
    global _pool
    if _pool:
        return _pool
    _pool = ThreadPoolExecutor(pool_size)
    return _pool
