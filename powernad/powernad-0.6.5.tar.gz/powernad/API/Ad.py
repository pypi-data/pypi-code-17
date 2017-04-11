import json
import jsonpickle
import pprint
from powernad.Connector.restapi import RestApi
from powernad.Object.Ad.AdObject import AdObject
class Ad: #광고 소재에 관한 API입니다.
    def __init__(self, base_url, api_key, secret_key, customer_id):
        self.r = RestApi(base_url, api_key, secret_key, customer_id)

    def get_ad_list_by_ids(self, ad_id):
        result = self.r.get('/ncc/ads', {'ids' : ad_id})
        adobj_list = []
        for arr in result:
            camp = AdObject(arr)
            adobj_list.append(camp)

        return adobj_list
        
    def get_ad_list(self, adgroup_id):
        result = self.r.get('/ncc/ads', {'nccAdgroupId' : adgroup_id})
        adobj_list = []
        for arr in result:
            camp = AdObject(arr)
            adobj_list.append(camp)

        return adobj_list

    def get_ad(self, ad_id):
        result = self.r.get('/ncc/ads/'+ad_id)
        result = AdObject(result)
        return result

    def create_ad(self, CreateAdObject):
        data = jsonpickle.encode(CreateAdObject, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = data
        data_str = json.dumps(data_str)
        print(data_str)
        result = self.r.post('/ncc/ads', data_str)
        result = AdObject(result)
        return result

    def update_ad(self, ad_id, fields, CreateAdObject):
        data = jsonpickle.encode(CreateAdObject, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = data
        data_str = json.dumps(data_str)
        result = self.r.put('/ncc/ads/'+ad_id, data_str,{'fields' : fields })
        pprint.pprint(result)
        result = AdObject(result)
        return result

    def delete_ad(self, ad_id):
        self.r.delete('/ncc/ads/'+ad_id)
        return True

    def copy_ad(self, ad_id, targetAdGroupId, userLock):
        query = {'ids' : ad_id, 'targetAdgroupId' : targetAdGroupId, 'userLock' : userLock}
        result = self.r.put('/ncc/ads', None, query)
        result = AdObject(result)
        return result
    def null_dict(self, input_dict):
        real = dict()
        for now in input_dict:
            if input_dict[now] != None:
                real.update({now :input_dict[now]})
        return real
