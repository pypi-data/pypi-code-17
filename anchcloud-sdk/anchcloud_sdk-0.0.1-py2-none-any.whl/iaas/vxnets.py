from anchcloud.conn.iaas_client import *
from anchcloud.misc.utils import *


class Vxnets(APIConnection):
    def __init__(self, connect):
        self.send_request = connect.send_request

    def list(self, zone, body=None):
        path = "/v2/zone/" + zone + "/vxnets"
        return self.send_request("GET", path, body)

    def create(self, zone, body):
        path = "/v2/zone/" + zone + "/vxnets"
        body = dict(body)
        if not check_params(body, required_params=["vxnet_name", "count"],
                            integer_params=["count"]):
            return None
        return self.send_request("POST", path, body)

    def modify(self, zone, vxnet_id, body):
        path = "/v2/zone/" + zone + "/vxnets/" + ",".join(vxnet_id)
        return self.send_request("PUT", path, body, return_result=False)

    def delete(self, zone, vxnet_id):
        path = "/v2/zone/" + zone + "/vxnets/" + ",".join(vxnet_id)
        print path
        return self.send_request("DELETE", path, None)

    def join(self, zone, body):
        path = "/v2/zone/" + zone + "/vxnets/join"
        body = dict(body)
        if not check_params(body, required_params=["vxnet", "instances"]):
            return None
        return self.send_request("POST", path, body)

    def leave(self, zone, body):
        path = "/v2/zone/" + zone + "/vxnets/leave"
        body = dict(body)
        if not check_params(body, required_params=["vxnet", "instances"]):
            return None
        return self.send_request("POST", path, body)
