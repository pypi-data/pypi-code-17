#!/usr/bin/env python3

"""
In your application configuration add:

[/]
tools.SATransaction.on = True

"""

import cherrypy

def clean_transaction():
    """Method that is called after the CherryPy request handler.
    Rollbacks all uncommitted changes.
    """
    from ..db import db
    if db.registry.has():  # cleanup is needed if there's some session only
        db.rollback()
        # deconfigure (unbind) session so it will be recreated for next request
        db.remove()


cherrypy.tools.SATransaction = cherrypy.Tool(
    point='on_end_resource',
    callable=clean_transaction,
    name='SATransaction',
    priority=80)
