from anchcloud.conn.iaas_client import *
from anchcloud.misc.utils import *


class Images(APIConnection):
    def __init__(self, connect):
        self.send_request = connect.send_request

    def list(self, zone, body=None):
        path = "/v2/zone/" + zone + "/images"
        return self.send_request("GET", path, body)

    def create(self, zone, body):
        path = "/v2/zone/" + zone + "/images"
        body = dict(body)
        if not check_params(body, required_params=["image_name", "instance"]):
            return None
        return self.send_request("POST", path, body)

    def modify(self, zone, body):
        path = "/v2/zone/" + zone + "/images"
        body = dict(body)
        if not check_params(body, required_params=["image"]):
            return None
        return self.send_request("PUT", path, body,return_result=False)

    def delete(self, zone, images):
        path = "/v2/zone/" + zone + "/images/" + ",".join(images)
        print path
        return self.send_request("DELETE", path, None)
