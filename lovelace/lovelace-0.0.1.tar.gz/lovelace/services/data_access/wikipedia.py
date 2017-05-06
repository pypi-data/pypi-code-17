from typing import (Any,
                    Dict)

from aiohttp import ClientSession

from lovelace.config import API_URL


async def query_wikipedia_api(*,
                              session: ClientSession,
                              **params: Dict[str, str]
                              ) -> Dict[str, Any]:
    params['format'] = 'json'
    params['action'] = 'query'
    async with session.get(API_URL,
                           params=params) as response:
        response_json = await response.json()
        return response_json
