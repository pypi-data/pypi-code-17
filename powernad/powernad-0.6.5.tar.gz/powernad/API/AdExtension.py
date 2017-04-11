import json
import jsonpickle
from powernad.Connector.restapi import RestApi
from powernad.Object.AdExtension.AdExtensionObject import AdExtensionObject
import pprint

class AdExtension: #확장소재 
    def __init__(self, base_url, api_key, secret_key, customer_id):
        self.r = RestApi(base_url, api_key, secret_key, customer_id)

    def get_ad_extensions_list(self, ownerId):
        result = self.r.get('/ncc/ad-extensions', {'ownerId' : ownerId})
        adext_list = []
        for arr in result:
            camp = AdExtensionObject(arr)
            adext_list.append(camp)
        return adext_list

    def get_ad_extensions_list_by_ids(self, ids):
        result = self.r.get('/ncc/ad-extensions', {'ids' : ids})
        adext_list = []
        for arr in result:
            camp = AdExtensionObject(arr)
            adext_list.append(camp)
        return adext_list

    def get_ad_extensions(self, adExtensionId):
        result = self.r.get('/ncc/ad-extensions/'+adExtensionId)
        result = AdExtensionObject(result)

        return result

    def create_ad_extensions(self, CreateAdExtensionObject):
        
        data = jsonpickle.encode(CreateAdExtensionObject, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = data
        data_str = json.dumps(data_str)
        
        result = self.r.post('/ncc/ad-extensions', data_str)
        result = AdExtensionObject(result)
        return result

    def update_ad_extensions(self, adExtensionId, fields, UpdateAdExtensionObject):
        
        data = jsonpickle.encode(UpdateAdExtensionObject, unpicklable=False)
        data = json.loads(data)
        data = self.null_dict(data)
        data_str = data
        data_str = json.dumps(data_str)
        pprint.pprint(data_str)
        query = {'fields' : fields}
        self.r.put('/ncc/ad-extensions/'+adExtensionId, data_str, query)
    
    def delete_ad_extensions(self, adExtensionId):
        self.r.delete('/ncc/ad-extensions/'+adExtensionId)
        return True

    def null_dict(self, input_dict):
        real = dict()
        for now in input_dict:
            if input_dict[now] != None:
                real.update({now :input_dict[now]})
        return real


    