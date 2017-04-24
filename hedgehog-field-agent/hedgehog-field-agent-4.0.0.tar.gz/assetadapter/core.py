import json
import logging
from threading import Lock

import datetime
from visa import ResourceManager


class ScVisaError(Exception):
    def __init__(self, message):
        self.ts = str(datetime.datetime.now())
        self.message = message
    def __str__(self):
        return '%s: %s' % (self.ts, self.message)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class VisaDeviceManager():
    def __init__(self, visa_library):
        """
        Constructor.
        :param visa_library: PyVISA backend library. 
        """
        self.lock = Lock()
        self.rm = ResourceManager(visa_library)

        self.lock.acquire()
        try:
            self.rm.list_resources()
        except Exception as ex:
            logging.exception("message")
            raise ScVisaError(str(ex))
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
                    logging.exception("message")
            return index
        except Exception as ex:
            logging.exception("message")
            raise ScVisaError(str(ex))
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
            logging.info("dm.query" + alias + ":" + command)
            resource = self.devices[alias]
            # return resource.query_ascii_values(command, container=numpy.array, separator=',')
            return resource.query(command)
        except Exception as ex:
            logging.exception("message")
            raise ScVisaError(str(ex))
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
            logging.info("dm.query_ascii" + alias + ":" + command)
            resource = self.devices[alias]
            return resource.query_ascii_values(command, container=numpy.array, separator=',')
        except Exception as ex:
            logging.exception("message")
            raise ScVisaError(str(ex))
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
            logging.info("dm.read" + alias + ":" + command)
            resource = self.devices[alias]
            return resource.read(command)
        except Exception as ex:
            logging.exception("message")
            raise ScVisaError(str(ex))
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
            logging.info("dm.write" + alias + ":" + command)
            resource = self.devices[alias]
            resource.write(command)
        except Exception as ex:
            logging.exception("message")
            raise ScVisaError(str(ex))
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
            logging.exception("message")
            raise ScVisaError(str(ex))
        finally:
            self.lock.release()