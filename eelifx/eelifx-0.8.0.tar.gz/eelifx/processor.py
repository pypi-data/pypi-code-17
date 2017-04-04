import json
import typing
import asyncio
import logging

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError

from eelifx.bulbs import Bulbs
from eelifx.luacode import luacode, statement_for
from eelifx.ship import Ship
from eelifx.lifx_commander import LifxCommander
from eelifx.transport import get_ship_status


def run_rules(
    lc_index: int,
    lifx_commanders: typing.List[LifxCommander],
    ship: Ship,
    rules: typing.Dict
):
    for rule in rules:
        logging.debug(rule)

        if eval(rule['statement_compiled']):
            exec(rule['effect_compiled'])


async def process_game_state(
    loop: asyncio.AbstractEventLoop,
    bulbs: Bulbs,
    lifx_commanders: typing.Sequence[LifxCommander],
    poll_interval: int,
    groups: typing.Dict,
    endpoint: str,
    ship: Ship=None,
):
    if ship is None:
        logging.info('Creating Ship object')
        ship = Ship()

    session = aiohttp.ClientSession()

    html = None
    try:
        html = await get_ship_status(session, endpoint)
    except ClientConnectorError as e:
        logging.warn("Unable to connect to EmptyEpsilon, is its http server running?")
        logging.warn(e)

    ship_data = None

    if html:
        try:
            ship_data = json.loads(html)
        except json.JSONDecodeError:
            logging.warning('Unable to parse EmptyEpsilon response')
        else:
            if 'ERROR' in ship_data.keys():
                if ship_data['ERROR'] == 'No game':
                    logging.info('EmptyEpsilon reports no game is running')
                else:
                    logging.critical('Error returned by EmptyEpsilon:%s' % ship_data['ERROR'])
                    logging.critical('Executed LUA:\n---%s---' % luacode())

                ship_data = None

    if ship_data:
        try:
            ship.update(ship_data)
        except Exception as e:
            raise
        else:
            logging.info(ship)

            for lc_index, group in enumerate(groups):
                lifx_commanders[lc_index].reset()
                exec(group['base_state_compiled'])

                run_rules(
                    lc_index,
                    lifx_commanders,
                    ship,
                    group['rules']
                )

                lifx_commanders[lc_index].apply(bulbs)

    session.close()
    await asyncio.sleep(poll_interval)
    asyncio.ensure_future(process_game_state(loop, bulbs, lifx_commanders, poll_interval, groups, endpoint, ship))


async def queryship(endpoint, hull=None, energy=None):
    session = aiohttp.ClientSession()
    insert = ''

    if hull:
        insert = f"{insert}{statement_for('hull', hull)}"

    if energy:
        insert = f"{insert}{statement_for('energy', energy)}"

    html = None
    try:
        html = await get_ship_status(session, endpoint, insert=insert)
    except ClientConnectorError as e:
        logging.warn("Unable to connect to EmptyEpsilon, is its http server running?")
        logging.warn(e)

    logging.info(f'Response\n{html}')
    session.close()
