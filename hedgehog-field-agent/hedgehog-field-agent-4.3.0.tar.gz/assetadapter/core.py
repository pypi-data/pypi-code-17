import json
import logging
from threading import Lock

import datetime

import numpy
from visa import ResourceManager

STATION_CONTROLLER_ERROR_CODE_VISA_ERROR = 111


class ScVisaError(StandardError):
    def __init__(self, status_code, message):
        Exception.__init__(self, status_code)  # <-- REQUIRED
        self.status_code = status_code
        self.ts = str(datetime.datetime.now())
        self.message = message

    # def __str__(self):
    #     return self.toJSON()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

_device_map = {}

class VisaDeviceManager():
    def __init__(self, visa_library):
        """
        Constructor.
        :param visa_library: PyVISA backend library. 
        """
        self.lock = Lock()
        self.rm = ResourceManager(visa_library)
        self.devices = _device_map
        self.lock.acquire()
        try:
            self.rm.list_resources()
        except Exception as ex:
            raise ScVisaError(status_code=STATION_CONTROLLER_ERROR_CODE_VISA_ERROR, message=ex.message)
        finally:
            self.lock.release()

    def alias(self, resource_mapping):
        """
        VISA alias command to make a friendly name to a resource.
        :param resource_mapping: Dictionary, keys are the friendly name, values are the VISA connection strings.
        :return: Count of connected elements.
        """
        index = 0
        self.lock.acquire()
        try:
            logging.info('Connectiong devices ...')
            for key, value in resource_mapping.items():
                try:
                    if any(value in s for s in self.rm.list_resources()):
                        res = self.rm.open_resource(value)
                        logging.info('<' + key + '> : ' + value)
                        self.devices[key] = res
                        index += 1
                except Exception as ex:
                    pass
            return index
        except Exception as ex:
            raise ScVisaError(status_code=STATION_CONTROLLER_ERROR_CODE_VISA_ERROR, message=ex.message)
        finally:
            self.lock.release()

    def query(self, alias, command):
        """
        VISA query command.
        :param alias: Asset friendly name.
        :param command: VISA query command.
        :return: Parsed result of the VISA query.
        """
        self.lock.acquire()
        try:
            resource = self.devices[alias]
            logging.info("VISA >> %s query %s" % (alias, command))
            result = resource.query(command)
            logging.debug("VISA << %s" % result)
        except Exception as ex:
            logging.error("VISA << %s" % ex)
            logging.exception("message")
            raise ScVisaError(status_code=STATION_CONTROLLER_ERROR_CODE_VISA_ERROR, message=ex.message)
        finally:
            self.lock.release()

    def query_ascii(self, alias, command):
        """
        VISA query command to ASCII nd-array.
        :param alias: Asset friendly name.
        :param command: VISA query command.
        :return: Parsed result of the VISA query.
        """
        self.lock.acquire()
        try:
            logging.info("dm.query_ascii " + alias + ":" + command)
            resource = self.devices[alias]
            return resource.query_ascii_values(command, container=numpy.array, separator=',')
        except Exception as ex:
            raise ScVisaError(status_code=STATION_CONTROLLER_ERROR_CODE_VISA_ERROR, message=ex.message)
        finally:
            self.lock.release()

    def read(self, alias, command):
        """
        VISA read command
        :param alias: Asset friendly name.
        :param command: VISA read command.
        :return: Parsed result of VISA command.
        """
        self.lock.acquire()
        try:
            logging.info("dm.read " + alias + ":" + command)
            resource = self.devices[alias]
            return resource.read(command)
        except Exception as ex:
            raise ScVisaError(status_code=STATION_CONTROLLER_ERROR_CODE_VISA_ERROR, message=ex.message)
        finally:
            self.lock.release()

    def write(self, alias, command):
        """
        VISA write command.
        :param alias: Asset friendly name.
        :param command: VISA write command.
        """
        self.lock.acquire()
        try:
            logging.info("dm.write " + alias + ":" + command)
            resource = self.devices[alias]
            resource.write(command)
            return
        except Exception as ex:
            raise ScVisaError(status_code=STATION_CONTROLLER_ERROR_CODE_VISA_ERROR, message=ex.message)
        finally:
            self.lock.release()

    def list(self):
        """
        List discoverable VISA resources.
        :return: Array of the connection strings.
        """
        self.lock.acquire()
        try:
            logging.info("dm.list")
            return self.rm.list_resources()
        except Exception as ex:
            raise ScVisaError(status_code=STATION_CONTROLLER_ERROR_CODE_VISA_ERROR, message=ex.message)
        finally:
            self.lock.release()
