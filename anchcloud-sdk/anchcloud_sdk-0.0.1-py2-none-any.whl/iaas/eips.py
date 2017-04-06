from anchcloud.conn.iaas_client import *
from anchcloud.misc.utils import *


class Eips(APIConnection):
    def __init__(self, connect):
        self.send_request = connect.send_request

    def list(self, zone, body=None):
        path = "/v2/zone/" + zone + "/eips"
        return self.send_request("GET", path, body)

    def create(self, zone, body, ):
        path = "/v2/zone/" + zone + "/eips"
        body = dict(body)
        if not check_params(body, required_params=["bandwidth", "eip_group", "count"],
                            integer_params=["bandwidth", "count"]):
            return None
        return self.send_request("POST", path, body)

    def modify(self, zone, eip_id, body):
        path = "/v2/zone/" + zone + "/eips/" + eip_id
        return self.send_request("PUT", path, body,return_result=False)

    def delete(self, zone, eip_id, force="false"):
        path = "/v2/zone/" + zone + "/eips/" + ",".join(eip_id)
        return self.send_request("DELETE", path, {"force": force})

    def assosiate(self, zone, body, force="false"):
        path = "/v2/zone/" + zone + "/eips/associate?" + "force=" + force
        body = dict(body)
        if not check_params(body, required_params=["eip", "instance"]):
            return None
        return self.send_request("POST", path, body)

    def dissociate(self, zone, body):
        path = "/v2/zone/" + zone + "/eips/dissociate"
        body = dict(body)
        if not check_params(body, required_params=["eips"]):
            return None
        return self.send_request("POST", path, body)

    def bandwidth(self, zone, body):
        path = "/v2/zone/" + zone + "/eips/bandwidth"
        body = dict(body)
        if not check_params(body, required_params=["eips", "bandwidth"], integer_params=["bondwidth"]):
            return None
        return self.send_request("POST", path, body)

    def groups(self, zone, body=None):
        path = "/v2/zone/" + zone + "/eip_groups"
        return self.send_request("GET", path, body)
