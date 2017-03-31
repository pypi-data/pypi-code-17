#!/usr/bin/env python

#
# Project:  juju-vnfm
# file:     asyncio_test
# created:  17/02/2017 
#

"""
description goes here
"""
import asyncio
import time
import traceback

from juju.model import Model


async def status():
    try:
        model = Model()
        await model.connect_current()

        print("model: %s" % model)

        print("applications %s" % model.applications)

        print(list(model.units.values())[0].data)

    except Exception as e:
        traceback.print_exc()
    finally:
        await model.disconnect()
        model.loop.stop()


loop = asyncio.get_event_loop()
loop.create_task(status())
loop.run_forever()
