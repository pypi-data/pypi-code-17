from anchcloud.conn.iaas_client import *
from anchcloud.misc.utils import *


class Routers(APIConnection):
    def __init__(self, connect):
        self.send_request = connect.send_request

    def list(self, zone, body=None):
        path = "/v2/zone/" + zone + "/routers"
        return self.send_request("GET", path, body)

    def create(self, zone, body):
        path = "/v2/zone/" + zone + "/routers"
        body = dict(body)
        if not check_params(body, required_params=["router", "nets", "eip", "router_type", "router_name", "bandwidth",
                                                   "eip_group"]):
            return None
        for i in range(len(body["nets"])):
            if not check_params(body["nets"][i], required_params=["ip_network"]):
                return None
            if not check_params(body["nets"][i], integer_params=["features"]):
                return None
        if not check_params(body["eip"], integer_params=["bandwidth"]):
            return None
        return self.send_request("POST", path, body)

    def modify(self, zone, router_id, body):
        path = "/v2/zone/" + zone + "/routers/" + router_id
        body = dict(body)
        if not check_params(body, required_params=["router_name", "description"]):
            return None
        return self.send_request("PUT", path, body,return_result=False)

    def delete(self, zone, router_id):
        path = "/v2/zone/" + zone + "/routers/" + ",".join(router_id)
        return self.send_request("DELETE", path, None)

    def power_on(self, zone, body):
        path = "/v2/zone/" + zone + "/routers/power_on"
        body = dict(body)
        if not check_params(body, required_params=["routers"]):
            return None
        return self.send_request("POST", path, body)

    def power_off(self, zone, body):
        path = "/v2/zone/" + zone + "/routers/power_off"
        body = dict(body)
        if not check_params(body, required_params=["routers"]):
            return None
        return self.send_request("POST", path, body)

    def update(self, zone, body):
        path = "/v2/zone/" + zone + "/routers/update"
        body = dict(body)
        if not check_params(body, required_params=["routers"]):
            return None
        return self.send_request("POST", path, body)

    def resize(self, zone, body):
        path = "/v2/zone/" + zone + "/routers/resize"
        body = dict(body)
        if not check_params(body, required_params=["routers", "router_type"]):
            return None
        return self.send_request("POST", path, body)

    def add_net(self, zone, body):
        path = "/v2/zone/" + zone + "/routers/nets"
        body = dict(body)
        if not check_params(body, required_params=["ip_network", "router"], integer_params=["features"]):
            return None
        return self.send_request("POST", path, body)

    def eip(self, zone, body):
        path = "/v2/zone/" + zone + "/routers/eips"
        body = dict(body)
        if not check_params(body, required_params=["eip", "router"]):
            return None
        return self.send_request("POST", path, body)

    def security_group(self, zone, body):
        path = "/v2/zone/" + zone + "/routers/security_groups"
        body = dict(body)
        if not check_params(body, required_params=["security_group", "router"]):
            return None
        return self.send_request("POST", path, body)

    def list_rule(self, zone, router_id, body=None):
        path = "/v2/zone/" + zone + "/routers/" + router_id + "/statics"
        return self.send_request("GET", path, body)

    def add_rule(self, zone, body):
        path = "/v2/zone/" + zone + "/routers/statics"
        body = dict(body)
        if not check_params(body, required_params=["router", "static_type"]):
            return None
        if body.has_key("port_forward_statics"):
            require = ["source_port", "target_ip", "target_port", "router_static_name"]
            for i in range(len(body["port_forward_statics"])):
                if not check_params(body["port_forward_statics"][i], required_params=require):
                    return None
        if body.has_key("vpn_statics"):
            require = ["vpn_type", "user_pwd", "connection_num", "router_static_name"]
            for i in range(len(body["vpn_statics"])):
                if not check_params(body["vpn_statics"][i], required_params=require, integer_params=["connection_num"]):
                    return None
        if body.has_key("dhcp_statics"):
            require = ["instance_id", "instance_id"]
            for i in range(len(body["dhcp_statics"])):
                if not check_params(body["dhcp_statics"][i], required_params=require):
                    return None
        if body.has_key("threegre_statics"):
            require = ["remoteip_ssh_p2plocalip_p2premoteip", "goalnet"]
            for i in range(len(body["threegre_statics"])):
                if not check_params(body["threegre_statics"][i], required_params=require):
                    return None
        if body.has_key("filter_control_statics"):
            require = ["source_ip", "source_port", "goal_ip", "goal_port", "action"]
            for i in range(len(body["filter_control_statics"])):
                if not check_params(body["filter_control_statics"][i], required_params=require):
                    return None
        if body.has_key("threeipsec_statics"):
            require = ["remoteip_way_remoteid", "localnet", "goalnet", "model"]
            for i in range(len(body["threeipsec_statics"])):
                if not check_params(body["threeipsec_statics"][i], required_params=require):
                    return None
        if body.has_key("dns_statics"):
            require = ["ip_address", "domain_name"]
            for i in range(len(body["dns_statics"])):
                if not check_params(body["dns_statics"][i], required_params=require):
                    return None
        if body.has_key("config_statics"):
            require = ["mss", ]
            for i in range(len(body["config_statics"])):
                if not check_params(body["config_statics"][i], required_params=require, integer_params=["mss"]):
                    return None
        return self.send_request("POST", path, body)

    def modify_rule(self, zone, router_static_id, body):
        path = "/v2/zone/" + zone + "/router_statics/" + router_static_id
        body = dict(body)
        if body.has_key("port_forward_static"):
            require = ["source_port", "target_ip", "target_port", "router_static_name"]
            if not check_params(body["port_forward_static"], required_params=require):
                return None
        if body.has_key("vpn_static"):
            require = ["vpn_type", "user_pwd", "connection_num", "router_static_name"]
            if not check_params(body["vpn_static"], required_params=require, integer_params=["connection_num"]):
                return None
        if body.has_key("dhcp_static"):
            require = ["instance_id", "instance_id"]
            if not check_params(body["dhcp_static"], required_params=require):
                return None
        if body.has_key("threegre_static"):
            require = ["remoteip_ssh_p2plocalip_p2premoteip", "goalnet"]
            if not check_params(body["threegre_static"], required_params=require):
                return None
        if body.has_key("filter_control_static"):
            require = ["source_ip", "source_port", "goal_ip", "goal_port", "action"]
            if not check_params(body["filter_control_static"], required_params=require):
                return None
        if body.has_key("threeipsec_static"):
            require = ["remoteip_way_remoteid", "localnet", "goalnet", "model"]
            if not check_params(body["threeipsec_static"], required_params=require):
                return None
        if body.has_key("dns_static"):
            require = ["ip_address", "domain_name"]
            if not check_params(body["dns_static"], required_params=require):
                return None
        if body.has_key("config_static"):
            require = ["mss", ]
            if not check_params(body["config_static"], required_params=require, integer_params=["mss"]):
                return None
        return self.send_request("PUT", path, body,return_result=False)

    def delete_rule(self, zone, router_static_id):
        path = "/v2/zone/" + zone + "/router_statics/" + ",".join(router_static_id)
        return self.send_request("DELETE", path, None)

    def list_network(self, zone, router_id, body=None):
        path = "/v2/zone/" + zone + "/routers/" + router_id + "/vxnets"
        return self.send_request("GET", path, body)

    def list_rule_entry(self, zone, router_static_id, body=None):
        path = "/v2/zone/" + zone + "/router_statics/" + router_static_id + "/entries"
        return self.send_request("GET", path, body)

    def add_rule_entry(self, zone, router_static_id, body):
        path = "/v2/zone/" + zone + "/router_statics/" + router_static_id + "/entries"
        body = dict(body)
        if body.has_key("vpn_static_entries"):
            require = ["user", "pwd"]
            for i in range(len(body["vpn_static_entries"])):
                if not check_params(body["vpn_static_entries"][i], required_params=require):
                    return None
        if body.has_key("gre_static_entries"):
            require = ["target_network"]
            for i in range(len(body["gre_static_entries"])):
                if not check_params(body["gre_static_entries"][i], required_params=require):
                    return None
        if body.has_key("ipsec_static_entries"):
            require = ["local_network", "target_network"]
            for i in range(len(body["ipsec_static_entries"])):
                if not check_params(body["ipsec_static_entries"][i], required_params=require):
                    return None
        return self.send_request("POST", path, body)

    def modify_rule_entry(self, zone, router_static_id, body):
        path = "/v2/zone/" + zone + "/router_static_entries/" + router_static_id
        body = dict(body)
        if body.has_key("vpn_static_entry"):
            require = ["user", "pwd"]
            if not check_params(body["vpn_static_entry"], required_params=require):
                return None
        if body.has_key("gre_static_entry"):
            require = ["target_network"]
            if not check_params(body["gre_static_entry"], required_params=require):
                return None
        if body.has_key("ipsec_static_entry"):
            require = ["local_network", "target_network"]
            if not check_params(body["ipsec_static_entry"], required_params=require):
                return None
        return self.send_request("PUT", path, body,return_result=False)

    def delete_rule_entry(self, zone, router_static_entry_id):
        path = "/v2/zone/" + zone + "/router_static_entries/" + ",".join(router_static_entry_id)
        return self.send_request("DELETE", path, None)
