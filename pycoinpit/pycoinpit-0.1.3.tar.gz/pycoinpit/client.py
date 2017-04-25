import requests
import crypto
from account import Account
from rest import Rest

class Client(object):
    def __init__(self, key=None, url=None):
        self.testnet_base_url = "https://live.coinpit.me/api/v1"
        self.livenet_base_url = "https://live.coinpit.io/api/v1"
        self.base_url_map = {0: self.livenet_base_url, 111: self.testnet_base_url}
        self.private_key = key
        self.account = None
        self.rest = None

        self.all = None
        self.contract = None

        if self.private_key is None:
            return
        self.network_code = crypto.get_network_code(self.private_key)
        self.base_url = url if url is not None else self.base_url_map[self.network_code]
        self.rest = Rest(self.base_url)

    def get_server_pubkey(self):
        if self.account is not None:
            return
        if self.private_key is None:
            raise ValueError('Private key needed for protected endpoints')
        user_pub_key = crypto.get_pub_key(self.private_key)
        auth_info = requests.get(self.base_url + "/auth/" + user_pub_key, headers={'Accept': 'application/json'}).json()
        if isinstance(auth_info, dict) and 'error' in auth_info.keys() is not None:
            raise RuntimeError('Error getting public key: ' + auth_info['error'])
        return auth_info['serverPublicKey']

    def connect(self):
        server_pub_key = self.get_server_pubkey()
        self.account = Account(self.private_key, server_pub_key)
        self.rest = Rest(self.base_url, self.account)


    def info(self):
        return self.rest.server_call("/all/info")

    def get_account(self):
        return self.rest.auth_server_call("GET", "/account")

    # def patch_orders(self, patch_spec):
    #     orders.patch(self, patch_spec)
    #
    # def cancel_orders(self, cancel_spec):
    #     orders.cancel(self, cancel_spec)
    #
    # def cancel_all_orders(self):
    #     orders.cancel_all(self)
    #
    # def update_orders(self, update_spec):
    #     orders.update(self, update_spec)
    #
    # def create_orders(self, create_spec):
    #     orders.create(self, create_spec)
    #
    # def get_open_orders(self, get_open_spec):
    #     orders.get_open(self, get_open_spec)
    #
    # def get_closed_orders(self, get_closed_spec):
    #     orders.get_closed(self, get_closed_spec)
    #
    # def get_cancelled_orders(self, get_cancelled_spec):
    #     orders.get_cancelled(self, get_cancelled_spec)

    def get_orders(self, instrument, status="open", after=None):
        uri = "/contract/" + instrument + "/order/" + status + ("" if after is None else "?after=" + after)
        result = self.rest.auth_server_call("GET", uri)
        return result
