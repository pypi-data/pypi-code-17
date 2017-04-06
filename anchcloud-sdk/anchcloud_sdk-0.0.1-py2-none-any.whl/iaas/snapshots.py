from anchcloud.conn.iaas_client import *
from anchcloud.misc.utils import *


class Snapshots(APIConnection):
    def __init__(self, connect):
        self.send_request = connect.send_request

    def list(self, zone, body=None):
        path = "/v2/zone/" + zone + "/snapshots"
        return self.send_request("GET", path, body)

    def create(self, zone, body):
        path = "/v2/zone/" + zone + "/snapshots"
        body = dict(body)
        if not check_params(body, required_params=["resources", "snapshot_name"]):
            return None
        return self.send_request("POST", path, body)

    def modify(self, zone, snapshot, body):
        path = "/v2/zone/" + zone + "/snapshots/" + snapshot
        body = dict(body)
        if not check_params(body, required_params=["description", "snapshot_name"]):
            return None
        return self.send_request("PUT", path, body, return_result=False)

    def delete(self, zone, snapshot):
        path = "/v2/zone/" + zone + "/snapshots/" + snapshot
        return self.send_request("DELETE", path, None)
