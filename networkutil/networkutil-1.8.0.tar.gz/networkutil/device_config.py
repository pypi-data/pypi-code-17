
import attr

import logging_helper
from _metadata import __version__, __authorshort__, __module_name__
from resources import templates, schema
from configurationutil import Configuration, cfg_params
from networkutil.endpoint_config import Endpoints

logging = logging_helper.setup_logging()

# Register Config details (These are expected to be overwritten by an importing app)
cfg_params.APP_NAME = __module_name__
cfg_params.APP_AUTHOR = __authorshort__
cfg_params.APP_VERSION = __version__

# Set the config initialisation parameters
DEVICE_CONFIG = u'device_config'

TEMPLATE = templates.devices
SCHEMA = schema.devices


# Device property keys
@attr.s(frozen=True)
class _DeviceConstant(object):
    name = attr.ib(default=u'name', init=False)
    ip = attr.ib(default=u'ip', init=False)
    port = attr.ib(default=u'port', init=False)
    active = attr.ib(default=u'active', init=False)
    default = attr.ib(default=u'default', init=False)

DeviceConstant = _DeviceConstant()


def _register_device_config():

    # Retrieve configuration instance
    cfg = Configuration()

    # Register configuration
    cfg.register(config=DEVICE_CONFIG,
                 config_type=cfg_params.CONST.json,
                 template=TEMPLATE,
                 schema=SCHEMA)

    return cfg


class Device(object):

    def __init__(self,
                 name,
                 ip,
                 port,
                 active,
                 default,
                 **parameters):

        self.name = name
        self.ip = ip
        self.port = port
        self.active = active
        self.default = default
        self.additional_attributes = self._extract_parameters(parameters)

    def _extract_parameters(self,
                            parameters):

        """
        Takes a dict of key value pairs and turns them into instance attributes

        :param dict parameters:

        :return:
        """

        # Set each parameter as an attribute
        for key, value in parameters.iteritems():
            setattr(self, key, value)

        return parameters

    def update(self):

        updated_device = self.__dict__.copy()

        del updated_device[DeviceConstant.name]
        del updated_device[u'additional_attributes']

        cfg = _register_device_config()
        key = u'{c}.{d}'.format(c=DEVICE_CONFIG,
                                d=self.name)
        cfg[key] = updated_device

    def get_endpoint(self,
                     api,
                     environment):
        return Endpoints().get_endpoint(api=api,
                                        environment=self.__dict__[environment])

    def __str__(self):
        return unicode(self)

    def __unicode__(self):
        string = (u'name: {name}\n'
                  u'address: {ip}:{port}\n'
                  u'active: {active}\n'
                  u'default: {default}\n'.format(name=self.name,
                                                 ip=self.ip,
                                                 port=self.port,
                                                 active=self.active,
                                                 default=self.default))

        for key, value in self.additional_attributes.iteritems():
            string += u'{key}: {value}\n'.format(key=key,
                                                 value=value)

        return string

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)


class Devices(object):

    @property
    def raw_devices(self):

        cfg = _register_device_config()
        devices = cfg[DEVICE_CONFIG]
        logging.debug(u'Devices: {e}'.format(e=devices))

        # Return a copy so that modifications of the retrieved do not get saved in config unless explicitly requested!
        return devices.copy()

    def __iter__(self):
        return iter(self.get_devices())

    def get_devices(self,
                    active_devices_only=False):

        devices = []

        for device_name, device in self.raw_devices.iteritems():

            if active_devices_only and not device[DeviceConstant.active]:
                # Device not active and we want active devices only
                continue

            devices.append(Device(name=device_name,
                                  **device))

        return devices

    def get_active_devices(self):
        return self.get_devices(active_devices_only=True)

    def get_device(self,
                   device=None,
                   active_devices_only=False,
                   suppress_refetch=False):

        # Check whether we have been passed the Device object
        if isinstance(device, Device):
            if suppress_refetch:
                return device

            # Set device to device name ready for re-fetch
            device = device.name

        if not device:
            return self.get_default_device()

        for dev in self.get_devices(active_devices_only=active_devices_only):
            if dev.name == device:
                return dev

            if dev.ip == device:
                return dev

            # Check all additional attributes for device reference
            for attribute in dev.additional_attributes.keys():
                if dev[attribute] == device:
                    return dev

        raise LookupError(u'Unable to find device: {device}'.format(device=device))

    def get_active_device(self,
                          **kwargs):
        return self.get_device(active_devices_only=True,
                               **kwargs)

    def get_default_device(self):

        default = [device for device in self.get_devices() if device.default]

        if len(default) == 1:
            return default[0]

        elif len(default) == 0:
            # If we get to here no default device is configured
            self._set_first_configured_device_as_default()
            return self.get_default_device()

        else:
            raise LookupError(u'More than one default Device is configured!')

    def get_default_device_or_first_configured(self):

        """
        Attempts to retrieve the default device.
        If no default device configured then it will return the first active device.
        If no active devices then it will return the first device it can get!
        """

        try:
            return self.get_default_device()

        except LookupError:

            try:
                return self.get_active_devices()[0]

            except IndexError:
                return self.get_devices()[0]

    def _set_first_configured_device_as_default(self):

        devices = self.get_devices()

        device = devices[0]
        device.default = True
        device.update()

        for device in devices[1:]:
            device.default = False
            device.update()

    @staticmethod
    def add_device(device_name,
                   device):

        cfg = _register_device_config()
        key = u'{c}.{i}'.format(c=DEVICE_CONFIG,
                                i=device_name)

        cfg[key] = device

    @staticmethod
    def delete_device(device_name):

        cfg = _register_device_config()
        key = u'{k}.{d}'.format(k=DEVICE_CONFIG,
                                d=device_name)
        del cfg[key]
