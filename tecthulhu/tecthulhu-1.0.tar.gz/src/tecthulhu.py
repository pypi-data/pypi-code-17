import argparse
import asyncio
import logging

from aiohttp import web

logger = logging.getLogger(__name__)

relay_mode = 0
relay_state = 1
portal_details = {
    'controllingFaction': '2',
    'level': 8,
    'health': 100,
    'title': 'Camp Navarro',
    'resonators': [
        {'level': 8, 'health': 100, 'owner': '__ADA__', 'position': 'E'},
        {'level': 8, 'health': 100, 'owner': '__ADA__', 'position': 'NE'},
        {'level': 8, 'health': 100, 'owner': '__ADA__', 'position': 'N'},
        {'level': 8, 'health': 100, 'owner': '__ADA__', 'position': 'NW'},
        {'level': 8, 'health': 100, 'owner': '__ADA__', 'position': 'W'},
        {'level': 8, 'health': 100, 'owner': '__ADA__', 'position': 'SW'},
        {'level': 8, 'health': 100, 'owner': '__ADA__', 'position': 'S'},
        {'level': 8, 'health': 100, 'owner': '__ADA__', 'position': 'SE'},
    ]
}

def refresh_relay_state():
    global relay_state

    if relay_mode == 0:
        pass
    elif relay_mode == 1:
        relay_state = int(portal_details['controllingFaction'] != '0')
    elif relay_mode == 2:
        relay_state = int(portal_details['controllingFaction'] == '0')
    elif relay_mode == 3:
        # TODO(honles): this has a time component
        relay_state = int(portal_details['controllingFaction'] != '0')
    elif relay_mode == 4:
        # TODO(honles): this has a time component
        relay_state = int(portal_details['controllingFaction'] != '0')
    else:
        raise RuntimeError('Relay mode %s not implemented!' % relay_mode)

@asyncio.coroutine
def diagnostics_handler(request):
    return web.Response(text=portal_details['title'])

@asyncio.coroutine
def relay_handler(request):
    global relay_mode, relay_state
    command = request.match_info['relay_command']

    if command == 'get_mode':
        return web.Response(text=str(relay_mode))

    if command == 'get_state':
        refresh_relay_state()
        return web.Response(text=str(relay_state))

    if command == 'set_manual':
        relay_mode = 0
        return web.Response(text='ok')

    if command.startswith('set_auto'):
        try:
            new_mode = int(command[8:])
        except ValueError:
            raise web.HTTPNotFound()

        if not (1 <= new_mode <= 4):
            raise web.HTTPNotFound()

        relay_mode = new_mode
        return web.Response(text='ok')

    if command == 'high':
        relay_mode = 0
        relay_state = 1
        return web.Response(text='ok')

    if command == 'low':
        relay_mode = 0
        relay_state = 0
        return web.Response(text='ok')

    if command == 'toggle':
        relay_mode = 0
        relay_state = int(not relay_state)
        return web.Response(text='ok')

    raise web.HTTPNotFound()

@asyncio.coroutine
def status_handler(request):
    status_type = request.match_info['status_type']
    if status_type == 'json':
        return web.json_response({'status': portal_details})

    if status_type == 'faction':
        return web.Response(text=portal_details['controllingFaction'])

    if status_type == 'health':
        return web.Response(text=portal_details['health'])

    if status_type == 'title':
        return web.Response(text=portal_details['title'])

    raise web.HTTPNotFound()

def main(host='0.0.0.0', port=8080, debug=False):
    app = web.Application(debug=debug)
    module_app = web.Application()
    command_app = web.Application()

    command_app.router.add_route('*', '/relay/{relay_command}', relay_handler)
    command_app.router.add_route('*', '/diagnostics', diagnostics_handler)

    module_app.add_subapp('/command', command_app)
    module_app.router.add_route('*', '/status/{status_type}', status_handler)

    app.add_subapp('/module', module_app)
    web.run_app(app, host=host, port=port)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        default=False, help='Enable debugging mode.')
    parser.add_argument('-p', '--port',
                        default=8080, type=int,
                        help='Port to start server on (default: 8080).')

    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARN)
    main(port=args.port, debug=args.debug)
