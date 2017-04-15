# import asyncio
# import aiohttp
# import logging
# import aiosocks
# from aiosocks import (
#     Socks4Addr, Socks5Addr, Socks4Auth, Socks5Auth,
#     HttpProxyAddr, HttpProxyAuth
# )
# from aiosocks.connector import SocksConnector
#
# logger = logging.getLogger('asyncio')
# logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)
#
#
# @asyncio.coroutine
# def test():
#     conn = SocksConnector(proxy=Socks5Addr('127.0.0.1'),
#                           proxy_auth=Socks5Auth('proxyuser1', 'password1'),
#                           remote_resolve=False, fingerprint=b'\xfc\xeb\xf8\t\xabg\xfd\xee\xae\xf2OY\xa6z\xcc,_\xa8\x84\xf2')
#     #conn = None
#     # conn = ProxyConnector(HttpProxyAddr('http://localhost:8080'),
#     #                       proxy_auth=HttpProxyAuth('proxyuser1', 'password1'))
#
#     with aiohttp.ClientSession(connector=conn) as session:
#         resp = yield from session.get('https://habrahabr.ru')
#         if resp.status == 200:
#             print((yield from resp.text()))
#         else:
#             print(resp.status)
#         resp.release()
#
#     # transport, protocol = yield from aiosocks.create_connection(
#     #     None, Socks5Addr('127.0.0.1'), Socks5Auth('proxyuser1', 'password1'),
#     #     dst=('habrahabr.ru', 80), remote_resolve=False
#     # )
#     # protocol.pause_writing()
#
#
# loop = asyncio.get_event_loop()
# loop.set_debug(1)
# loop.run_until_complete(test())
# loop.close()


import asyncio
import aiohttp
import aiosocks
from aiosocks.connector import SocksConnector
import logging

async def check_proxy(timeout, loop=None):
    proxy = ('127.0.0.1', 1080)
    url = 'http://google.com/'
    addr = aiosocks.Socks5Addr(proxy[0], proxy[1])
    auth = aiosocks.Socks5Auth('proxyuser2', 'password2')
    conn = SocksConnector(proxy=addr, proxy_auth=auth, remote_resolve=True, loop=loop)
    try:
        with aiohttp.ClientSession(loop=loop, connector=conn) as session:
            session._cookie_jar.update_cookies({'a': 'b'})
            async with session.get(url) as response:
                    html = await response.text()
                    logging.info(html)
    except asyncio.TimeoutError:
        logging.info('TimeoutError')
        return 'fail'


def main():
    loop = asyncio.get_event_loop()
    # loop.set_debug(enabled=True)
    for timeout in range(1):
        asyncio.ensure_future(check_proxy(timeout, loop=loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        exit()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s')
    main()
