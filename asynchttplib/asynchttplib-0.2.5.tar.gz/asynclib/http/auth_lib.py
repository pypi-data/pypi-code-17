from aiohttp.web import BaseRequest

from asynclib.amqp.client import AMQPClient
from asynclib.http.error import BaseError


def parse_token(request, token_key='auth_token'):
    """

    :type request: BaseRequest
    """
    auth_token = None
    auth_header = request.headers.get('Authorization')
    if auth_header is not None and auth_header.lower().startswith('bearer '):
        auth_token = auth_header.split(' ')[1].strip()
    elif request.query.get(token_key):
        auth_token = request.query.get(token_key)
    elif request.cookies.get(token_key):
        auth_token = request.cookies.get(token_key)
    return auth_token


async def parse_user(request, service, endpoint, token_key='auth_token'):
    """
    :type token_key: str
    :type endpoint: str
    :type service: str
    :type request: BaseRequest
    """
    auth_token = parse_token(request, token_key)
    if auth_token is not None:
        try:
            async with AMQPClient(service) as client:
                user = await client.call(endpoint, **{token_key: auth_token})
            return user
        except BaseError:
            return None
    else:
        return None