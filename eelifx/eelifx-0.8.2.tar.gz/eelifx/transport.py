import async_timeout

from eelifx.luacode import luacode


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def get_ship_status(session, url, insert=None):
    with async_timeout.timeout(10):
        async with session.post(url, data=luacode(insert)) as response:
            return await response.text()
