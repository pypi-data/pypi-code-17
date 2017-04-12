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
        subnets_dict = dict()
        _subnets = data['subnets']
        for subnet in _subnets['subnets']:
            subnets_dict.update({subnet['subnet']: {'cidr': subnet['cidr'],
                                                    'vpc': subnet['vpc'],
                                                    'az': subnet['az']}})
        return subnets_dict

    def _acls(self, data):
        acls_dict = dict()
        _acls = data['acls']
        tags_acl = _acls['tags']
        acl_assoc = {acl["aclassoc"]: {'subnet': acl['subnet'],
                                       'acl': acl['acl']} for acl in _acls['associations']}
        for acl in _acls['acls']:
            tag = next((item for item in tags_acl if item["id"] == acl['acl']), {
                       'key': '', 'value': ''})
            acls_dict.update(
                {acl['acl']: self._merge_dicts({"vpc": acl['vpc']}, tag)})
        return {'acl_vpc': acls_dict, 'assoc': acl_assoc}

    def _eni(self, data):
        _enis = data['enis']
        sg_enis = self._mk_item_list(_enis['sgs'], 'sg', 'eni')
        instance_enis = {item['eni']: item['instance']
                         for item in _enis['attachments']}
        return sg_enis, instance_enis

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
        all_sg = dict()
        for tag in sg_tags:
            name = self.mk_pp_name(tag)
            vpc = sg_vpc[tag['id']]
            all_sg.update({tag['id']: {'name': name, 'vpc': vpc}})
        return all_sg

    def _instances(self, data):
        """
        Deal with Instances data
        return a dictionary of instances
        """
        _instances = data['instances']
        instance_dict = dict()
        for inst in _instances["instances"]:
            instance_dict.update(
                {inst['instance']: {'subnet': inst['subnet']}})
        tags_dict = {t['id']: {'Key': t['key'],
                               'Value': t['value']} for t in _instances['tags']}
        all_dict = dict()
        for id, val in instance_dict.items():
            key_value_tags = {'Key': '', 'Value': ''}
            try:
                all_dict.update({id: self._merge_dicts(tags_dict[id], val)})
            except:
                all_dict.update({id: self._merge_dicts(key_value_tags, val)})
        return all_dict

    def _merge_dicts(self, *dict_args):
        """
        merge dicts
        """
        result = dict()
        for dictionary in dict_args:
            result.update(dictionary)
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

    def all_vsi(self, vpc, subnet, instances):
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
                        if i_value['subnet'] == s:
                            all_instance.update({i: {'key': i_value['Key'],
                                                     'value': i_value['Value']}})
                    all_subnet.update({s: {'cidr': s_value['cidr'],
                                           'az': s_value['az'],
                                           'instances': all_instance}})
            v_value.update({'subnets': all_subnet})
            snapshot_data.update({v: v_value})
        return snapshot_data

    def mk_vsi(self, vsi_data):
        """
        Make VPC-Subnet-Instance Data
        """
        nodes, links = list(), list()
        for vpc, vpc_value in vsi_data.items():
            vpc_prop = {'cidr': vpc_value['cidr'],
                        'color': 'vpc',
                        'state': vpc_value['state']}
            vpc_node = {'id': vpc,
                        'properties': vpc_prop}
            nodes.append(vpc_node)
            for s, s_value in vpc_value['subnets'].items():
                v_link = {"source": vpc,
                          "target": s,
                          "properties": {"vpc": vpc,
                                         "type": "vpc_link"}}
                s_prop = {'cidr': s_value['cidr'],
                          'color': 'subnet',
                          'vpc': vpc,
                          'az': s_value['az']}
                sub_node = {'id': s,
                            'properties': s_prop}
                nodes.append(sub_node)
                links.append(v_link)
                for i, i_value in s_value['instances'].items():
                    s_link = {"source": s,
                              "target": i,
                              "properties": {"subnet": s, "type": "subnet_link"}}
                    i_name = self.mk_pp_name(i_value)
                    i_prop = {'vpc': vpc,
                              'subnet': s,
                              'color': 'instance',
                              'name': i_name}
                    i_node = {'id': i,
                              'properties': i_prop}
                    nodes.append(i_node)
                    links.append(s_link)
        d3json = {"label": "Tiros Snapshot Visualization",
                  "Snapshot View": "VPC-Subnet-Instance",
                  "links": links,
                  "nodes": nodes}
        return d3json

    def mk_acl(self, acl_dict):
        """
        Make ACLS-VPC-Subnet-Instance Data
        """
        nodes, links = list(), list()
        acl_vpc = acl_dict['acl_vpc']
        acl_assoc = acl_dict['assoc']
        for acl, acl_value in acl_vpc.items():
            i_name = self.mk_pp_name(acl_value)
            acl_prop = {'vpc': acl_value['vpc'],
                        'color': 'acl',
                        'name': i_name}
            acl_node = {'id': acl,
                        'properties': acl_prop}
            nodes.append(acl_node)
            for assoc, assoc_value in acl_assoc.items():
                if assoc_value['acl'] == acl:
                    assoc_link = {"source": acl,
                                  "target": assoc_value["subnet"],
                                  "properties": {"vpc": acl_value["vpc"],
                                                 "subnet": assoc_value["subnet"],
                                                 "type": "assoc_link"}}
                    assoc_prop = {'subnet': assoc_value['subnet'],
                                  'color': 'subnet',
                                  "acl_assoc": assoc,
                                  'vpc': acl_value["vpc"]}
                    subnet_node = {'id': assoc_value["subnet"],
                                   'properties': assoc_prop}
                    nodes.append(subnet_node)
                    links.append(assoc_link)
        d3json = {"label": "Tiros Snapshot Visualization",
                  "Snapshot View": "ACL-VPC-Subnet view",
                  "links": links,
                  "nodes": nodes}
        return d3json

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
            f.close()
        vpcs_dict = self._vpcs(parsed_json)
        self.dprint("VPCS", vpcs_dict)
        subnet_dict = self._subnets(parsed_json)
        self.dprint("Subnets", subnet_dict)
        instance_dict = self._instances(parsed_json)
        self.dprint("Instances", instance_dict)
        all_acls = self._acls(parsed_json)
        self.dprint("ACLS", all_acls)
        all_vsi = self.all_vsi(vpcs_dict, subnet_dict, instance_dict)
        vsi_data = self.mk_vsi(all_vsi)
        acls_data = self.mk_acl(all_acls)
        return vsi_data, acls_data

    def update_color(self, color, query_result, vsi_data):
        """
        Update node color based on query result
        """
        new_viz = vsi_data
        nodes = new_viz['nodes']
        for k in nodes:
            if k['id'] in query_result:
                prop = k['properties']
                prop.update({'color': color})
        return new_viz

    def mk_path_inline(self, dir, data):
        viz_filepath = os.path.join(dir, "viz_data", "inlineQuery.json")
        try:
            os.remove(viz_filepath)
        except Exception as e:
            pass
        with open(viz_filepath, 'w') as fp:
            json.dump(data, fp)
        print('Saved in {}'.format(viz_filepath))
        rel = os.path.relpath(viz_filepath)
        return rel.split('tiros_viz/')[1]
