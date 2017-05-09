import os
import pytest


@pytest.mark.run_loop
def test_aioredis_debug_env_var():
    os.environ['AIOREDIS_DEBUG'] = 'x'
    import aioredis
    conn = yield from aioredis.create_connection(('localhost', 6379))
    try:
        pass
    finally:
        conn.close()
        yield from conn.wait_closed()
