from anchcloud.conn.iaas_client import *
from anchcloud.misc.utils import *


class Instances(APIConnection):
    def __init__(self, connect):
        self.send_request = connect.send_request

    def list(self, zone, body=None):
        path = "/v2/zone/" + zone + "/instances"
        return self.send_request("GET", path, body)

    def create(self, zone, body):
        path = "/v2/zone/" + zone + "/instances"
        body = dict(body)
        require = ['instance', 'zone', 'image_id', 'cpu', 'memory', 'count']
        temp_body = body["instance"]
        if temp_body.has_key("instance_type"):
            require.remove('cpu')
            require.remove('memory')
        if temp_body.has_key("login_mode"):
            if temp_body["login_mode"] == "passwd":
                require.append('login_passwd')
            if temp_body["login_mode"] == "keypair":
                require.append('login_keypair')
        if not check_params(body, required_params=require):
            return None
        if not check_params(body["instance"], integer_params=["cpu", "memory", "count", "size"]):
            return None
        if body.has_key("volume"):
            for i in range(len(body["volume"])):
                if not check_params(body["volume"][i], required_params=["size"],
                                    integer_params=["size"]):
                    return None
        if body.has_key("vxnet"):
            if not check_params(body["vxnet"], required_params=["vxnet_type"]):
                return None
        if body.has_key("eip"):
            if not check_params(body["eip"], required_params=["bandwidth", "eip_group"],
                                integer_params=["bandwidth"]):
                return None

        return self.send_request("POST", path, body)

    def modify(self, zone, body):
        path = "/v2/zone/" + zone + "/instances"
        body = dict(body)
        if not check_params(body, required_params=["instances"]):
            return None
        return self.send_request("PUT", path, body, return_result=False)

    def start(self, zone, body):
        path = "/v2/zone/" + zone + "/instances/start"
        return self.send_request("POST", path, body)

    def stop(self, zone, body):
        path = "/v2/zone/" + zone + "/instances/stop"
        return self.send_request("POST", path, body)

    def restart(self, zone, body):
        path = "/v2/zone/" + zone + "/instances/restart"
        return self.send_request("POST", path, body)

    def reset(self, zone, body):
        path = "/v2/zone/" + zone + "/instances/reset"
        body = dict(body)
        require = ['instances']
        if body.has_key("login_mode"):
            if body["login_mode"] == "passwd":
                require.append('login_passwd')
            if body["login_mode"] == "keypair":
                require.append('login_keypair')
        if not check_params(body, required_params=require):
            return None
        return self.send_request("POST", path, body)

    def reset_password(self, zone, body):
        path = "/v2/zone/" + zone + "/instances/reset_password"
        body = dict(body)
        if not check_params(body, required_params=["instances", "login_passwd"]):
            return None
        return self.send_request("POST", path, body)

    def resize(self, zone, body):
        path = "/v2/zone/" + zone + "/instances/resize"
        body = dict(body)
        if not check_params(body, required_params=["instances"], integer_params=["cpu", "memory"]):
            return None
        return self.send_request("POST", path, body)

    def brokers(self, zone, instance_id):
        path = "/v2/zone/" + zone + "/instances/" + instance_id + "/brokers"
        return self.send_request("GET", path, None)

    def delete(self, zone, instances):
        if len(instances) > 1:
            raise APIError("", "The API only support one item.")
        path = "/v2/zone/" + zone + "/instances/" + ",".join(instances)
        return self.send_request("DELETE", path, None)
