from anchcloud.conn.iaas_client import *
from anchcloud.misc.utils import *


class Loadbalancers(APIConnection):
    def __init__(self, connect):
        self.send_request = connect.send_request

    def list(self, zone, body=None):
        path = "/v2/zone/" + zone + "/loadbalancers"
        return self.send_request("GET", path, body)

    def create(self, zone, body):
        path = "/v2/zone/" + zone + "/loadbalancers"
        body = dict(body)
        if not check_params(body, required_params=["loadbalancer", "vxnet"]):
            return None
        if not check_params(body["loadbalancer"], integer_params=["node_count"]):
            return None
        if body.has_key("eip"):
            if not check_params(body["eip"], required_params=["bandwidth", "eip_group", "count"],
                                integer_params=["bandwidth", "count"]):
                return None
        return self.send_request("POST", path, body)

    def modify(self, zone, loadbalancer_id, body):
        path = "/v2/zone/" + zone + "/loadbalancers/" + loadbalancer_id
        return self.send_request("PUT", path, body, return_result=False)

    def delete(self, zone, loadbalancer_id, delete_eips=None):
        path = "/v2/zone/" + zone + "/loadbalancers/" + loadbalancer_id
        return self.send_request("DELETE", path, {"delete_eips": ",".join(delete_eips)})

    def list_listeners(self, zone, loadbalancer_id, body=None):
        path = "/v2/zone/" + zone + "/loadbalancers/" + loadbalancer_id + "/listeners"
        return self.send_request("GET", path, body)

    def create_listener(self, zone, body):
        path = "/v2/zone/" + zone + "/loadbalancers/listeners"
        body = dict(body)
        if not check_params(body, required_params=["loadbalancer", "listeners"]):
            return None
        for i in range(len(body["listeners"])):
            if not check_params(body["listeners"][i],
                                required_params=["listener_port", "listener_protocol", "backend_protocol"],
                                integer_params=["listener_port", "forwardfor", "listener_option"]):
                return None
        return self.send_request("POST", path, body)

    def modify_listener(self, zone, loadbalancer_listener_id, body):
        path = "/v2/zone/" + zone + "/loadbalancers_listeners/" + loadbalancer_listener_id
        body = dict(body)
        if not check_params(body, integer_params=["listener_port", "forwardfor", "listener_option"]):
            return None
        return self.send_request("PUT", path, body, return_result=False)

    def delete_listener(self, zone, loadbalancer_listener_id):
        path = "/v2/zone/" + zone + "/loadbalancers_listeners/" + ",".join(loadbalancer_listener_id)
        return self.send_request("DELETE", path, None)

    def associate_eips(self, zone, body):
        path = "/v2/zone/" + zone + "/loadbalancers/associate_eips"
        body = dict(body)
        if not check_params(body, required_params=["eips", "loadbalancer"]):
            return None
        return self.send_request("POST", path, body)

    def dissociate_eips(self, zone, body):
        path = "/v2/zone/" + zone + "/loadbalancers/dissociate_eips"
        body = dict(body)
        if not check_params(body, required_params=["eips", "loadbalancer"]):
            return None
        return self.send_request("POST", path, body)

    def resize(self, zone, body):
        path = "/v2/zone/" + zone + "/loadbalancers/resize"
        body = dict(body)
        if not check_params(body, required_params=["loadbalancer_type", "Loadbalancers"]):
            return None
        return self.send_request("POST", path, body)

    def change_node(self, zone, body):
        path = "/v2/zone/" + zone + "/loadbalancers/change_node"
        body = dict(body)
        if not check_params(body, required_params=["node_count", "loadbalancer"], integer_params=["node_count"]):
            return None
        return self.send_request("POST", path, body)

    def apply(self, zone, body):
        path = "/v2/zone/" + zone + "/loadbalancers/apply"
        body = dict(body)
        if not check_params(body, required_params=["loadbalancers"]):
            return None
        return self.send_request("POST", path, body)

    def stop(self, zone, body):
        path = "/v2/zone/" + zone + "/loadbalancers/stop"
        body = dict(body)
        if not check_params(body, required_params=["loadbalancers"]):
            return None
        return self.send_request("POST", path, body)

    def start(self, zone, body):
        path = "/v2/zone/" + zone + "/loadbalancers/start"
        body = dict(body)
        if not check_params(body, required_params=["loadbalancers"]):
            return None
        return self.send_request("POST", path, body)

    def security_groups(self, zone, body):
        path = "/v2/zone/" + zone + "/loadbalancers/security_groups"
        return self.send_request("POST", path, body)

    def list_listeners_backends(self, zone, loadbalancer_listener_id, body=None):
        path = "/v2/zone/" + zone + "/loadbalancers_listeners/" + loadbalancer_listener_id + "/backends"
        return self.send_request("GET", path, body, return_result=True)

    def create_listeners_backends(self, zone, body):
        path = "/v2/zone/" + zone + "/loadbalancers_listeners/backends"
        if not check_params(body, required_params=["loadbalancer_listener", "backends"]):
            return None
        if body.has_key("backends"):
            for i in range(len(body["backends"])):
                if not check_params(body["backends"][i], required_params=["resource", "vxnet", "port", "weight"],
                                    integer_params=["port", "weight"]):
                    return None
        return self.send_request("POST", path, body)

    def modify_listeners_backends(self, zone, loadbalancer_backend_id, body):
        path = "/v2/zone/" + zone + "/loadbalancers_listener_backends/" + loadbalancer_backend_id
        if not check_params(body, integer_params=["port", "weight", "disabled", "loadbalancer_policy"]):
            return None
        return self.send_request("PUT", path, body, return_result=False)

    def delete_listeners_backends(self, zone, loadbalancer_backend_id):
        path = "/v2/zone/" + zone + "/loadbalancers_listener_backends/" + ",".join(loadbalancer_backend_id)
        return self.send_request("DELETE", path, None)

    def list_policies(self, zone, body=None):
        path = "/v2/zone/" + zone + "/loadbalancer_policies"
        return self.send_request("GET", path, body, return_result=True)

    def create_policies(self, zone, body):
        path = "/v2/zone/" + zone + "/loadbalancer_policies"
        return self.send_request("POST", path, body)

    def modify_policies(self, zone, loadbalancer_policy_id, body):
        path = "/v2/zone/" + zone + "/loadbalancer_policies/" + loadbalancer_policy_id
        return self.send_request("PUT", path, body, return_result=False)

    def delete_policies(self, zone, loadbalancer_policy_id):
        path = "/v2/zone/" + zone + "/loadbalancer_policies/" + ",".join(loadbalancer_policy_id)
        return self.send_request("DELETE", path, None)

    def apply_policies(self, zone, body):
        path = "/v2/zone/" + zone + "/loadbalancer_policies/apply"
        return self.send_request("POST", path, body)

    def list_policies_rules(self, zone, body=None):
        path = "/v2/zone/" + zone + "/loadbalancer_policies/apply/policy_rules"
        return self.send_request("GET", path, body)

    def create_policies_rules(self, zone, body):
        path = "/v2/zone/" + zone + "/loadbalancer_policy_rules"
        if not check_params(body, required_params=["loadbalancer_policy", "rules"]):
            return None
        for i in range(len(body["rules"])):
            if not check_params(body["rules"][i], required_params=["rule_type", "val"]):
                return None
        return self.send_request("POST", path, body)

    def modify_policies_rules(self, zone, loadbalancer_policy_rule_id, body):
        path = "/v2/zone/" + zone + "/loadbalancer_policy_rules/" + loadbalancer_policy_rule_id
        return self.send_request("PUT", path, body, return_result=False)

    def delete_policies_rules(self, zone, loadbalancer_policy_rule_id):
        path = "/v2/zone/" + zone + "/loadbalancer_policy_rules/" + ",".join(loadbalancer_policy_rule_id)
        return self.send_request("DELETE", path, None)

    def list_server_certificates(self, zone, body=None):
        path = "/v2/zone/" + zone + "/server_certificates"
        return self.send_request("GET", path, body)

    def create_server_certificates(self, zone, body):
        path = "/v2/zone/" + zone + "/server_certificates"
        if not check_params(body, required_params=["certificate_content", "private_key"]):
            return None
        return self.send_request("POST", path, body)

    def modify_server_certificates(self, zone, sc_id, body):
        path = "/v2/zone/" + zone + "/server_certificates/" + sc_id
        return self.send_request("PUT", path, body, return_result=False)
        # todo service_cert interface_error

    def delete_server_certificates(self, zone, sc_id):
        path = "/v2/zone/" + zone + "/server_certificates/" + ",".join(sc_id)
        return self.send_request("DELETE", path, None)
