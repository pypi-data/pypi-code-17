def create_aiohttp_app(routes, middlewares=[]):
    from aiohttp.web import Application

    application = Application(middlewares=middlewares)

    for url, handler in routes:
        application.router.add_get(url, handler)

    return application
