from anchcloud.conn.iaas_client import *
from anchcloud.misc.utils import *


class Keypairs(APIConnection):
    def __init__(self, connect):
        self.send_request = connect.send_request

    def list(self, zone, body=None):
        path = "/v2/zone/" + zone + "/keypairs"
        return self.send_request("GET", path, body)

    def create(self, zone, body):
        path = "/v2/zone/" + zone + "/keypairs"
        return self.send_request("POST", path, body)

    def modify(self, zone, keypair_id, body):
        path = "/v2/zone/" + zone + "/keypairs/" + keypair_id
        return self.send_request("PUT", path, body, return_result=False)

    def delete(self, zone, keypair_id, force="false"):
        path = "/v2/zone/" + zone + "/keypairs/" + ",".join(keypair_id)
        return self.send_request("DELETE", path, {"force": force})

    def list_instances(self, zone, keypair_id, body=None):
        path = "/v2/zone/" + zone + "/keypairs/" + keypair_id + "/instances"
        return self.send_request("GET", path, body)

    def attach(self, zone, body):
        path = "/v2/zone/" + zone + "/keypairs/attach"
        body = dict(body)
        if not check_params(body, required_params=["keypairs", "instances"]):
            return None
        return self.send_request("POST", path, body)

    def detach(self, zone, body):
        path = "/v2/zone/" + zone + "/keypairs/detach"
        if not check_params(body, required_params=["keypairs", "instances"]):
            return None
        return self.send_request("POST", path, body)
