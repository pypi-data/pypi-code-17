import sys
import signal
import typing
import asyncio
import logging
from functools import partial

import yaml
from yaml.scanner import ScannerError
import aiolifx

from eelifx.util import wait_for_members, marshal_commanders, shutdown_loop, normalise_endpoint
from eelifx.bulbs import Bulbs

from .processor import queryship

DEFAULT_CONFIG = {
    'poll_interval': 5,
    'wait_for_members': True,
    'groups': [
        {
            'match': '.*',
            'max_luminance': 0.29,
            'colour_temp': 3500,
            'base_state': '''
lifx_commanders[lc_index].set_power(True)
lifx_commanders[lc_index].set_colour("white")
lifx_commanders[lc_index].set_luminance(1.0)
''',
            'rules': [
                {
                    'statement': 'ship.energy > 0.6',
                    'effect': '''
lifx_commanders[lc_index].set_power(True)
lifx_commanders[lc_index].set_luminance(1.0)
''',
                },
                {
                    'statement': 'ship.energy < 0.4 and ship.energy >= 0.15',
                    'effect': '''
lifx_commanders[lc_index].set_power(True)
lifx_commanders[lc_index].set_luminance(0.6)
''',
                },
                {
                    'statement': 'ship.energy < 0.15 and ship.energy >= 0.05',
                    'effect': '''
lifx_commanders[lc_index].set_power(True)
lifx_commanders[lc_index].set_luminance(0.1)
''',
                },
                {
                    'statement': 'ship.energy < 0.05',
                    'effect': 'lifx_commanders[lc_index].set_power(False)',
                },
                {
                    'statement': "ship.alert_level == 'normal'",
                    'effect': "lifx_commanders[lc_index].set_colour('white')",
                },
                {
                    'statement': "ship.alert_level == 'YELLOW ALERT'",
                    'effect': '''
lifx_commanders[lc_index].set_colour('yellow')
lifx_commanders[lc_index].set_waveform({'waveform': 'SAW', 'hz': 0.5, 'alt_colour': 'white' })
''',
                },
                {
                    'statement': "ship.alert_level == 'RED ALERT'",
                    'effect': '''
lifx_commanders[lc_index].set_colour('red')
lifx_commanders[lc_index].set_waveform({'waveform': 'SAW', 'hz': 0.5, 'alt_colour': 'white' })
''',
                },
                {
                    'statement': 'ship.hull < 0.2 and ship.hull > 0.1',
                    'effect': '''
lifx_commanders[lc_index].set_power(True)
lifx_commanders[lc_index].set_waveform({'waveform': 'SAW', 'hz':5, 'alt_colour':'black', 'duty_cycle':0.9})
''',
                },
                {
                    'statement': 'ship.hull < 0.1',
                    'effect': 'lifx_commanders[lc_index].set_power(False)',
                },
            ]
        },
    ],
}

UDP_BROADCAST_PORT = 56700


def setup_logging(level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(level)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # create formatter
    formatter = logging.Formatter('%(asctime)s:%(name)s:[%(levelname)s]: %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)


def dump_config():
    return yaml.dump(DEFAULT_CONFIG, default_flow_style=False)


def display_config():
    print(dump_config())


def load_config(f_handle: typing.io):
    config = None

    try:
        config = yaml.load(f_handle.read())
    except ScannerError as e:
        logging.error(f'Unable to load config: {e}')
    finally:
        f_handle.close()

    return config


def setup_loop(
    mode: str,
    config=None,
    endpoint=None,
    loglevel=logging.DEBUG
):
    setup_logging(loglevel)

    if config is None:
        config = DEFAULT_CONFIG
    else:
        config = load_config(config)

    if config is None:
        sys.exit(1)

    if mode == 'run' and endpoint is None:
        logging.error('Must supply an endpoint!')
        sys.exit(1)

    if endpoint:
        config['endpoint'] = normalise_endpoint(endpoint)

    MyBulbs = Bulbs()

    lifx_commanders = marshal_commanders(config)
    #  Initialise the event loop
    loop = asyncio.get_event_loop()
    coro = loop.create_datagram_endpoint(
        partial(aiolifx.LifxDiscovery, loop, MyBulbs),
        local_addr=('0.0.0.0', UDP_BROADCAST_PORT)
    )

    try:
        loop.create_task(coro)
        asyncio.ensure_future(
            wait_for_members(
                loop,
                MyBulbs,
                lifx_commanders,
                config['poll_interval'],
                config,
                mode=mode
            )
        )
        logging.info("Use Ctrl-C to quit")
        loop.add_signal_handler(signal.SIGHUP, partial(shutdown_loop, loop))
        loop.add_signal_handler(signal.SIGTERM, partial(shutdown_loop, loop))
        loop.run_forever()
    except (SystemExit, KeyboardInterrupt):
        pass
    except Exception:
        logging.error()
    finally:
        shutdown_loop(loop)
        loop.stop()
        loop.run_forever()
        loop.close()


def setup_queryship(endpoint: str, hull: int=None, energy: int=None, loglevel=logging.DEBUG):
    setup_logging()
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGHUP, partial(shutdown_loop, loop))
    loop.add_signal_handler(signal.SIGTERM, partial(shutdown_loop, loop))
    loop.run_until_complete(queryship(normalise_endpoint(endpoint), hull=hull, energy=energy))
