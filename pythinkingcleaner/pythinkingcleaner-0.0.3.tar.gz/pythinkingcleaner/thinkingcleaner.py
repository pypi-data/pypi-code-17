import requests

DISCOVERY_URL = 'https://thinkingsync.com/api/v1/discover/devices'
EP_STATUS = 'status.json'
EP_DETAIL_STATUS = 'full_status.json'
EP_COMMAND = 'command.json?command='


class ThinkingCleaner(object):
    def __init__(self, ip, uuid):
        self.ip = ip
        self.uuid = uuid
        self.base_uri = 'http://' + self.ip + '/'
        self.name = 'unknown'
        self.uuid = 'unknown'
        self.status = 'st_unknown'
        self.is_cleaning = False
        self.battery = 0
        self.capacity = 0

        self.update()

    def update(self):
        response = requests.get(self.base_uri + EP_STATUS)
        status = response.json()
        status = status['status']

        self.name = status['name']
        self.battery = status['battery_charge']
        self.capacity = status['capacity']
        self.status = status['cleaner_state']
        self.is_cleaning = status['cleaning'] == '1'

    def send_command(self, command):
        response = requests.get(self.base_uri + EP_COMMAND + command)
        result = response.json()

    def start_cleaning(self):
        if self.is_cleaning:
            return

        self.send_command('clean')
        self.is_cleaning = True

    def stop_cleaning(self):
        if not self.is_cleaning:
            return

        self.send_command('clean')
        self.is_cleaning = False

    def dock(self):
        self.send_command('dock')

    def find_me(self):
        self.send_command('find_me')

    def restart(self):
        self.send_command('crash')



