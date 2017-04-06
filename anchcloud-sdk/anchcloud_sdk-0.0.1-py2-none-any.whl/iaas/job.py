from anchcloud.conn.iaas_client import *
from anchcloud.misc.utils import *


class Job(APIConnection):
    def __init__(self, connect):
        self.send_request = connect.send_request

    def status(self, zone, job_id, body=None):
        path = "/v2/zone/" + zone + "/job/" + job_id
        return self.send_request("GET", path, body)

    def lease(self, zone, body):
        path = "/v2/zone/" + zone + "/lease"
        return self.send_request("POST", path, body)