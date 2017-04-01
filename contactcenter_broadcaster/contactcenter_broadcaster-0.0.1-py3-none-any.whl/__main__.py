"""
Enter point for appliaction.
"""

# DEJA VU SANS MONO

if __name__ == '__main__':
    import asyncio
    import uvloop

    # set alternative event loop
    # very IMPORTANT do it for first,
    # before everything others import`s,
    # except asyncio and uvloop
    asyncio.set_event_loop(uvloop.new_event_loop())

    from os.path import dirname, abspath, isfile
    from contactcenter_broadcaster.configuration import print_meta, make_config
    from contactcenter_broadcaster.logger import configure as logger_configure
    import aiohttp_debugger

    RESOURCES_DIR = "%s/resources" % dirname(abspath(__file__))
    CONFIG_FILE_NAME = 'config.yaml'
    CONFIG_FILE_DIRS = '/etc/contactcenter', '/opt/contactcenter', RESOURCES_DIR

    config, loaded_url = make_config(CONFIG_FILE_NAME, CONFIG_FILE_DIRS)

    logger_configure(config['logger'])
    print_meta(loaded_url)

    from aiohttp.web import run_app as run_aiohttp_app
    from contactcenter_broadcaster import create_aiohttp_app
    from contactcenter_broadcaster.controller import routes
    from contactcenter_broadcaster.worker import run_workers

    application = create_aiohttp_app(routes)
    aiohttp_debugger.Debugger.instance(application)

    run_workers()
    run_aiohttp_app(
        application,
        host=config['application']['host'],
        port=int(config['application']['port'])
    )
