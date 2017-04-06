from anchcloud.conn.iaas_client import *
from anchcloud.misc.utils import *


class Volumes(APIConnection):
    def __init__(self, connect):
        self.send_request = connect.send_request

    def list(self, zone, body=None):
        path = "/v2/zone/" + zone + "/volumes"
        return self.send_request("GET", path, body)

    def create(self, zone, body):
        path = "/v2/zone/" + zone + "/volumes"
        if not check_params(body, required_params=["size"], integer_params=["size", "count"]):
            return None
        return self.send_request("POST", path, body)

    def modify(self, zone, voluemes, body):
        path = "/v2/zone/" + zone + "/volumes/" + ",".join(voluemes)
        if not check_params(body, required_params=["volume_name", "description"]):
            return None
        return self.send_request("PUT", path, body,return_result=False)

    def delete(self, zone, volumes):
        if len(volumes) > 1:
            raise APIError("", "The API only support one item.")
        path = "/v2/zone/" + zone + "/volumes/" + ",".join(volumes)
        return self.send_request("DELETE", path, None)

    def resize(self, zone, body):
        path = "/v2/zone/" + zone + "/volumes/resize"
        if not check_params(body, required_params=["volumes", "size"], integer_params=["size"]):
            return None
        return self.send_request("POST", path, body)

    def attach(self, zone, body):
        path = "/v2/zone/" + zone + "/volumes/attach"
        if not check_params(body, required_params=["instance_id", "volumes"]):
            return None
        return self.send_request("POST", path, body)

    def detach(self, zone, body):
        path = "/v2/zone/" + zone + "/volumes/detach"
        if not check_params(body, required_params=["instance_id", "volumes"]):
            return None
        return self.send_request("POST", path, body)
