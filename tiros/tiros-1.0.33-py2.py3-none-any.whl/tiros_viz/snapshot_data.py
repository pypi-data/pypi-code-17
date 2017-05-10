import os
import glob
import subprocess
import json
import pprint


class SData(object):
    """
    Parse Tiros Snapshot json data
    """

    def __init__(self, debug):
        self.debug = debug
        return

    def dprint(self, msg, data):
        if self.debug:
            print("--start--{}".format(msg))
            pprint.pprint(data)
            print("--end--{}".format(msg))

    def _vpcs(self, data):
        vpc_dict = dict()
        vpcs = data['vpcs']
        vpcs_tags = vpcs['tags']
        for tag in vpcs_tags:
            vpc_dict.update({tag['vpc']: {'state': tag['state'],
                                          'cidr': tag['cidr']}})
        return vpc_dict

    def _subnets(self, data):
        subnets = dict()
        _subnets = data['subnets']
        for subnet in _subnets['subnets']:
            subnets.update({subnet['subnet']: {'cidr': subnet['cidr'],
                                               'vpc': subnet['vpc'],
                                               'az': subnet['az']}})
        return subnets

    def _acls(self, data):
        acls = dict()
        _acls = data['acls']
        tags_acl = _acls['tags']
        acl_assoc = {acl["aclassoc"]: {'subnet': acl['subnet'],
                                       'acl': acl['acl']} for acl in _acls['associations']}
        for acl in _acls['acls']:
            tag = next((item for item in tags_acl if item["id"] == acl['acl']), {
                       'key': '', 'value': ''})
            acls.update(
                {acl['acl']: self._merge_dicts({"vpc": acl['vpc']}, tag)})
        return {'acl_vpc': acls, 'assoc': acl_assoc}

    def _eni(self, data):
        _enis = data['enis']
        sg_enis = self._mk_item_list(_enis['sgs'], 'sg', 'eni')
        ips = {d['eni']: {'ip': d['ip']} for d in _enis['ips']}
        eni_pp = dict()
        for d in _enis["associations"]:
            p_p_ip = {i: d[i] for i in d if i != 'eni'}
            eni_pp.update({d['eni']: p_p_ip})
        instance_enis = {item['instance']: item['eni']
                         for item in _enis['attachments']}
        eni_detail = self._merge_dicts(ips, eni_pp)
        return sg_enis, instance_enis, eni_detail

    def _elbs(self, data):
        data_elbs = data['elbs']
        sg_elb = {item['sg']: item['elb'] for item in data_elbs['sgs']}
        sg_subnet = {item['elb']: item['subnet']
                     for item in data_elbs['subnets']}
        elb_tags = {item['id']: item['value'] for item in data_elbs['tags']}
        elb_instance = self._mk_item_list(
            data_elbs['instances'], 'instance', 'elb')
        return elb_instance

    def _sg(self, data):
        acls_dict = dict()
        data_sgs = data['sgs']
        sg_tags = data_sgs['tags']
        sg_vpc = {item['sg']: item['vpc'] for item in data_sgs['sgs']}
        sg_egress = self.mk_egress(data_sgs["custom-cidrs"])
        sg_ingress = self.mk_ingress(data_sgs["tcp-udp-cidrs"])
        all_sg = dict()
        for tag in sg_tags:
            name = self.mk_pp_name(tag)
            sg = tag['id']
            vpc = sg_vpc[sg]
            egress = sg_egress.get(sg, {})
            ingress = sg_ingress.get(sg, {})
            sg_detail = {"name": name,
                         "vpc": vpc,
                         "egress": egress,
                         "ingress": ingress}
            all_sg.update({sg: sg_detail})
        return all_sg

    def _igws(self, data):
        _data = data["igws"]
        _attach = _data.get('attachments')
        _tags = _data.get('tags')
        igw_out = dict()
        for item in _attach:
            igw_out.update({item['igw']: {'vpc': item['vpc'],
                                          'state': item['state']}})
        for item in _tags:
            igw_item = igw_out.get(item['id'])
            name = self.mk_pp_name(item)
            igw_item.update({'name': name})
        return igw_out

    def get_tags(self, id, tags):
        tag_out = {tag['key']: tag['value'] for tag in tags if tag["id"] == id}
        return tag_out

    def mk_egress(self, custom_cidrs):
        out = dict()
        for d in custom_cidrs:
            rule = {i: d[i] for i in d if i not in ['sg', 'dir']}
            out.update({d['sg']: rule})
        return out

    def mk_ingress(self, tcp_udp_cidrs):
        out = dict()
        for item in tcp_udp_cidrs:
            port = item["ports"]
            pp = "%s-%s" % (port.get("from", ""), port.get("to", ""))
            rule = {i: item[i]
                    for i in item if i not in ['ports', 'dir', 'sg']}
            rule.update({"ports": pp})
            out.update({item["sg"]: rule})
        return out

    def _instances(self, data):
        """
        Deal with Instances data
        return a dictionary of instances
        """
        _instances = data['instances']
        inst_subnet = _instances.get('instance-subnets')
        _subnets = dict()
        if inst_subnet:
            _subnets = {sub['instance']: sub['subnet'] for sub in inst_subnet}
        instance_dict = dict()
        for inst in _instances["instances"]:
            instance = inst['instance']
            tags = self.get_tags(instance, _instances['tags'])
            sub = _subnets[instance] if _subnets else inst['subnet']
            instance_dict.update({instance: {'subnet': sub,
                                             'tags': tags}})
        return instance_dict

    def _merge_dicts(self, *dict_args):
        result = dict()
        for d in dict_args:
            result.update(d)
        return result

    def _mk_item_list(self, in_list, i_key, i_val):
        out = dict()
        for d in in_list:
            try:
                val = out[d[i_key]]
                val.append(d[i_val])
                out.update({d[i_key]: val})
            except:
                out.update({d[i_key]: [d[i_val]]})
        return out

    def all_vsi(self, vpc, subnet, instances, sg_eni):
        """
        Gather all data in one dictionary for VSI view
        """
        snapshot_data = dict()
        for v, v_value in vpc.items():
            all_subnet = dict()
            for s, s_value in subnet.items():
                if s_value['vpc'] == v:
                    all_instance = dict()
                    for i, i_value in instances.items():
                        sg = sg_eni[i]['sg']
                        i_sg = " ".join(x for x in sg)
                        i_eni = sg_eni[i]['eni']
                        if i_value['subnet'] == s:
                            all_instance.update({i: {'tags': i_value['tags'],
                                                     'sg': i_sg,
                                                     'eni': i_eni}})
                    all_subnet.update({s: {'cidr': s_value['cidr'],
                                           'az': s_value['az'],
                                           'instances': all_instance}})
            v_value.update({'subnets': all_subnet})
            snapshot_data.update({v: v_value})
        return snapshot_data

    def mk_instance_sg(self, sg_enis, instance_enis):
        eni_sg = dict()
        for sg, eni in sg_enis.items():
            for e in eni:
                try:
                    e_sg = eni_sg[e] + [sg]
                    eni_sg.update({e: e_sg})
                except:
                    eni_sg.update({e: [sg]})
        instance_sg_eni = dict()
        for k, v in instance_enis.items():
            instance_sg_eni.update({k: {"sg": eni_sg.get(v, []),
                                        "eni": v}})
        return instance_sg_eni

    def mk_pp_name(self, val_dict):
        if val_dict['key'] == 'Name':
            return val_dict['value']
        else:
            return "{}:{}".format(val_dict['key'], val_dict["value"])

    def process_snapshot(self, filename):
        """
        Read the Tiros Snapshot
        """
        parsed_json = None
        with open(filename) as f:
            parsed_json = json.load(f)
        vpcs_dict = self._vpcs(parsed_json)
        self.dprint("VPCS", vpcs_dict)
        subnet_dict = self._subnets(parsed_json)
        self.dprint("Subnets", subnet_dict)
        instance_dict = self._instances(parsed_json)
        self.dprint("Instances", instance_dict)
        acl_data = self._acls(parsed_json)
        self.dprint("ACLS", acl_data)
        sg_enis, instance_enis, eni_detail = self._eni(parsed_json)
        self.dprint("ENIS", instance_enis)
        igws = self._igws(parsed_json)
        self.dprint("IGWS", igws)
        sg_detail = self._sg(parsed_json)
        instance_sg_eni = self.mk_instance_sg(sg_enis, instance_enis)
        all_vsi = self.all_vsi(vpcs_dict, subnet_dict,
                               instance_dict, instance_sg_eni)
        return {'vsi': all_vsi,
                'acl': acl_data,
                'sg': sg_detail,
                'eni': eni_detail,
                'igws': igws}
