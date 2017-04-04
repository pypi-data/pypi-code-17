import logging
import os
import re

import click
import click_log
import gi
import yaml

gi.require_version('GUdev', '1.0')
gi.require_version('CScreensaver', '1.0')

from gi.repository import CScreensaver, Gio, GLib, GUdev
from xdg import BaseDirectory

logger = logging.getLogger(__name__)


@click.command()
@click.option('--init', is_flag=True)
@click_log.simple_verbosity_option()
@click_log.init(__name__)
def locker(init):
    config = os.path.join(
        BaseDirectory.save_config_path('cinnamon-udev-locker'),
        'config.yml'
    )
    try:
        with open(config) as f:
            conditions = yaml.load(f)
    except FileNotFoundError as e:
        logger.error('File not found {0}'.format(e.filename))
        return
    except PermissionError as e:
        logger.error('Unable to read file: {0}'.format(e.filename))
        return

    cs = CScreensaver.ScreenSaverProxy.new_for_bus_sync(
        Gio.BusType.SESSION,
        Gio.DBusProxyFlags.NONE,
        'org.cinnamon.ScreenSaver',
        '/org/cinnamon/ScreenSaver',
        None
    )

    def lock(device):
        logger.info('Lock: {0}'.format(device))
        cs.call_lock('{0} removed'.format(device.get_property('ID_MODEL_FROM_DATABASE')))

    def wakeup(device):
        logger.info('Wakeup: {0}'.format(device))
        cs.call_simulate_user_activity()

    actions = {
        'lock': lock,
        'wakeup': wakeup,
    }

    def match_device_properties(device, d):
        result = [re.match(p, device.get_property(k)) for k, p in d.items() if device.has_property(k)]
        return result and all(result)

    def event(client, action, device):
        if init:
            props = map(lambda k: '{0}: {1}'.format(k, device.get_property(k)), device.get_property_keys())
            print('{0}:\n * {1}'.format(action, '\n * '.join(props)))
            return
        for condition in conditions:
            try:
                result = [match_device_properties(device, d) for d in condition['devices']]

                if result and any(result):
                    if action in condition:
                        actions[condition[action]](device)
            except KeyError as e:
                logger.error('Invalid configuration')

    c = GUdev.Client(subsystems=[])
    c.connect('uevent', event)
    GLib.MainLoop().run()
