import json
import jsonpickle
import pprint
from powernad.Connector.restapi import RestApi
from powernad.Object.IpExclusion.IpExclusionObject import IpExclusionObject

class IpExclusion:
    def __init__(self, base_url, api_key, secret_key, customer_id):
        self.r = RestApi(base_url, api_key, secret_key, customer_id)

    def get_ip_exclusion(self):
        result = self.r.get('/tool/ip-exclusions')

        ip_exclusion_list = []
        for arr in result:
            ipex = IpExclusionObject(arr)
            ip_exclusion_list.append(ipex)

        return ip_exclusion_list

    def create_ip_exclusion(self, CreateIpExclusionObject):
        data = jsonpickle.encode(CreateIpExclusionObject, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = json.dumps(data)

        result = self.r.post('/tool/ip-exclusions', data_str)
        result = IpExclusionObject(result)

        return result

    def update_ip_exclusion(self, UpdateIpExclusionObject):
        data = jsonpickle.encode(UpdateIpExclusionObject, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = json.dumps(data)

        result = self.r.put('/tool/ip-exclusions', data_str)
        result = IpExclusionObject(result)

        return result

    def delete_ip_exclusion(self, id):
        result = self.r.delete('/tool/ip-exclusions/'+id)
        result = IpExclusionObject(result)

        return result

    def delete_ip_exclusion_many(self, id_array):
        query = {'ids' : id_array}
        self.r.delete('/tool/ip-exclusions', query)

        return True

    def null_dict(self, input_dict):
        real = dict()
        for now in input_dict:
            if input_dict[now] != None:
                real.update({now :input_dict[now]})
        return real