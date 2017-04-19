import requests
from .thinkingcleaner import ThinkingCleaner

DISCOVERY_URL = "https://thinkingsync.com/api/v1/discover/devices"


class Discovery(object):

    @staticmethod
    def discover():
        response = requests.get(url=DISCOVERY_URL)
        data = response.json()

        devices = []

        for device in data:
            devices.append(ThinkingCleaner(device['local_ip'], device['uuid']))

        return devices

