import json
import pprint


class D3Data(object):
    """
    Manipulate D3 Data
    """

    def __init__(self, debug):
        self.debug = debug
        return

    def mk_vsi(self, data):
        """
        Make VPC-Subnet-Instance-IGW D3 Data
        """
        vsi_data = data['vsi']
        sg_detail = data['sg']
        eni_detail = data['eni']
        igw = data['igws']
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
                              "properties": {"subnet": s,
                                             "type": "subnet_link"}}
                    i_name = self.mk_inst_name(i_value)
                    sg_id = i_value.get('sg', 'NotFound')
                    sg = sg_detail.get(sg_id, {})
                    eni_id = i_value.get('eni', 'NotFound')
                    eni = eni_detail.get(eni_id, {})
                    sg.update({'id': sg_id})
                    eni.update({'id': eni_id})
                    i_prop = {'vpc': vpc,
                              'subnet': s,
                              'color': 'instance',
                              'name': i_name,
                              'sg': sg,
                              'eni': eni}
                    i_node = {'id': i,
                              'properties': i_prop}
                    nodes.append(i_node)
                    links.append(s_link)
        igw_node, igw_link = self.mk_igw(igw)
        nodes += igw_node
        links += igw_link
        d3json = {"label": "Tiros Snapshot Visualization",
                  "Snapshot View": "VPC-Subnet-Instance",
                  "links": links,
                  "nodes": nodes}
        return d3json

    def mk_igw(self, igws):
        nodes, links = list(), list()
        for igw, val in igws.items():
            prop = {'name': val.get('name', 'NoName'),
                    'state': val.get('state', 'Unknown'),
                    'color': 'igw'}
            nodes.append({'id': igw,
                          'properties': prop})
            igw_link = {"source": igw,
                        "target": val['vpc'],
                        "properties": {"type": "igw_link"}}
            links.append(igw_link)
        return nodes, links

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

    def mk_inst_name(self, val_dict):
        tags = val_dict['tags']
        name = tags.get('Name', '')
        return name
