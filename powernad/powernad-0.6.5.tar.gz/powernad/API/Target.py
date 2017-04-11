import json
import jsonpickle
import pprint
from powernad.Connector.restapi import RestApi
from powernad.Object.Target.TargetObject import TargetObject

class Target:
    def __init__(self, base_url, api_key, secret_key, customer_id):
        self.r = RestApi(base_url, api_key, secret_key, customer_id)

    def get_target_list(self, ownerId, types=None):
        result = self.r.get('/ncc/targets', {'ownerId' : ownerId, 'types' : types})
        
        target_list = []
        for arr in result:
            target = TargetObject(arr)
            target_list.append(target)

        return target_list

    def update_target(self, targetId, UpdateTargetObject):

        data = jsonpickle.encode(UpdateTargetObject, unpicklable=False)
        data = json.loads(data)
        data = self.null_dict(data)
        data_str = json.dumps(data)

        result = self.r.put('/ncc/targets/'+targetId, data_str)

        result = TargetObject(result)
        return result

    def null_dict(self, input_dict):
        real = dict()
        for now in input_dict:
            if input_dict[now] != None:
                real.update({now :input_dict[now]})
        return real