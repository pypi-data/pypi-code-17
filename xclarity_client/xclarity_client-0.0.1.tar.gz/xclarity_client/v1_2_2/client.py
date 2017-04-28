import json
import requests
from .power_status import power_status_list, power_status_action
from .boot_order import boot_order_priority, setting_boot_type
from ..exceptions import *


requests.packages.urllib3.disable_warnings()


class Client(object):
    def __init__(self, username=None, password=None,
                 version=None, url=None):

        self._version = version
        self._username = username
        self._password = password
        self._url = url[:-1] if url is not None and url[-1] == '/' \
            else url

    def _gen_node_action_url(self, node_id):
        return '{url}/node/{node_id}'.format(url=self._url, node_id=node_id)

    def _get_node_details(self, node_id):
        url = self._gen_node_action_url(node_id)
        try:
            r = requests.get(url,
                             auth=(self._username, self._password),
                             verify=False,
                             timeout=(10, 10))
            result = {
                'status_code': r.status_code,
                'encoding': r.encoding,
                'headers': r.headers,
                'body': r.json()
            }
            return result
        except Exception as ex:
            NodeDetailsException(message=str(ex), node_id=node_id)

    def get_node_status(self, node_id):
        response = self._get_node_details(node_id)
        if response['status_code'] == 200:
            return response['body']['accessState'].lower()
        else:
            return 'unknown'

    def get_node_info(self, node_id):
        response = self._get_node_details(node_id)
        info = {}
        if response['status_code'] == 200:
            body = response['body']
            info['uuid'] = body.get('uuid', None)
            info['name'] = body.get('hostname', 'Unknown')
            info['power_state'] = power_status_list.get(
                body.get('powerStatus', 0), 0)

            info['chassis_id'] = None  # nullable
            info['target_power_state'] = None  # nullable
            info['provision_state'] = None   # nullable
            info['target_provision_state'] = None  # nullable
            info['provision_updated_at'] = None  # nullable
            info['last_error'] = None  # nullable
            info['instance_uuid'] = None  # nullable
            info['instance_info'] = None  # nullable

            info['raid_config'] = body.get('raidSettings', [])  # An array
            info['target_raid_config'] = []
            info['maintenance'] = False \
                if body.get('accessState', 'unknown') == 'online' else True
            info['maintenance_reason'] = None  # nullable
            info['console_enabled'] = False  # False is by default, what's this
            info['extra'] = {}  # What's this?
            info['properties'] = {}  # What's this?
        else:
            err_msg = "Fail to get node info, http status code is %s, " \
                      "http response is %s" % (response.status_code, response.content)
            raise NodeDetailsException(node_id=node_id, details=err_msg)

        return info

    def get_node_power_status(self, node_id):
        response = self._get_node_details(node_id)
        if response['status_code'] == 200:
            return power_status_list[response['body']['powerStatus']]
        else:
            return 'unknown'

    def set_node_power_status(self, node_id, action):
        if action not in power_status_action:
            raise BadPowerStatusSettingException(action=action)
        action = power_status_action[action]

        url = self._gen_node_action_url(node_id)
        data = {'powerState': action}
        r = requests.put(url,
                         auth=(self._username, self._password),
                         data=json.dumps(data),
                         verify=False)

        if r.status_code != 200:
            raise FailToSetPowerStatusException(node_id=node_id, action=action)

    def get_node_all_boot_info(self, node_id):
        response = self._get_node_details(node_id)
        if response['status_code'] == 200:
            return {'bootOrder': response['body']['bootOrder']}

    def get_node_boot_info(self, node_id):
        response = self._get_node_details(node_id)
        if response['status_code'] == 200:
            boot_order_list = response['body']['bootOrder']['bootOrderList']

            for boot_order in boot_order_list:
                type_name = boot_order['bootType'].lower()
                for item in boot_order_priority:
                    if item['name'] == type_name:
                        item['value'] = boot_order

            final_boot_order = None
            for item in boot_order_priority:
                if item['value'] is not None:
                    final_boot_order = item['value']
                    break

            return final_boot_order

        else:
            return None

    def set_node_boot_info(self, node_id, boot_order):
        # for item in boot_order['bootOrder']['bootOrderList']:
        #     if item['bootType'] in setting_boot_type:
        #         item['bootType'] = setting_boot_type[item['bootType']]

        try:
            url = self._gen_node_action_url(node_id)
            r = requests.put(url,
                             auth=(self._username, self._password),
                             data=json.dumps(boot_order),
                             verify=False)
            if r.status_code != 200:
                raise Exception("Fail to set node boot info. status code = %s" % r.status_code)
        except Exception as ex:
            print("Exception! - %s" % str(ex))
