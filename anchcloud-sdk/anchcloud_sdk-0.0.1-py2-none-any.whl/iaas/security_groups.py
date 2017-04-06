from anchcloud.conn.iaas_client import *
from anchcloud.misc.utils import *


class Security_groups(APIConnection):
    def __init__(self, connect):
        self.send_request = connect.send_request

    def list(self, zone, body=None):
        path = "/v2/zone/" + zone + "/security_groups"
        return self.send_request("GET", path, body)

    def create(self, zone, body):
        path = "/v2/zone/" + zone + "/security_groups"
        return self.send_request("POST", path, body)

    def modify(self, zone, security_group_id, body):
        path = "/v2/zone/" + zone + "/security_groups/" + ",".join(security_group_id)
        if not check_params(body, required_params=["security_group_name"]):
            return None
        return self.send_request("PUT", path, body, return_result=False)

    def delete(self, zone, security_group_id):
        path = "/v2/zone/" + zone + "/security_groups/" + ",".join(security_group_id)
        return self.send_request("DELETE", path, None)

    def associate(self, zone, security_group_id, body):
        path = "/v2/zone/" + zone + "/security_groups/" + security_group_id + "/instances"
        return self.send_request("POST", path, body)

    def list_snapshots(self, zone, security_group_id, body=None):
        path = "/v2/zone/" + zone + "/security_groups/" + security_group_id + "/snapshots"
        return self.send_request("GET", path, body, return_result=True)

    def create_snapshots(self, zone, body):
        path = "/v2/zone/" + zone + "/security_group_snapshots"
        if not check_params(body, required_params=["security_group"]):
            return None
        return self.send_request("POST", path, body)

    def delete_snapshots(self, zone, snap_id):
        path = "/v2/zone/" + zone + "/security_group_snapshots/" + ",".join(snap_id)
        return self.send_request("DELETE", path, None)

    def rollback_snapshots(self, zone, snap_id, body):
        path = "/v2/zone/" + zone + "/security_group_snapshots/" + snap_id + "/rollback"
        return self.send_request("POST", path, body)

    def list_rules(self, zone, body=None):
        path = "/v2/zone/" + zone + "/security_group_rules"
        return self.send_request("GET", path, body, return_result=True)

    def create_rules(self, zone, body):
        path = "/v2/zone/" + zone + "/security_group_rules"
        body = dict(body)
        if not check_params(body, required_params=["security_group"]):
            return None
        for i in range(len(body["rules"])):
            if not check_params(body["rules"][i], required_params=["protocol", "action", "direction", "name"]):
                return None
            if not check_params(body["rules"][i], integer_params=["priority", "disabled", "direction"]):
                return None
        return self.send_request("POST", path, body)

    def modify_rules(self, zone, security_group_rule_id, body):
        path = "/v2/zone/" + zone + "/security_group_rules/" + security_group_rule_id
        body = dict(body)
        if not check_params(body, required_params=["protocol", "priority", "action", "direction", "name"],
                            integer_params=["priority", "disabled", "direction"]):
            return None
        return self.send_request("PUT", path, body, return_result=False)

    def delete_rules(self, zone, security_group_rule_id):
        path = "/v2/zone/" + zone + "/security_group_rules/" + ",".join(security_group_rule_id)
        return self.send_request("DELETE", path, None)
