import json
import jsonpickle
import pprint
from powernad.Connector.restapi import RestApi
from powernad.Object.AdKeyword.AdKeywordObject import AdKeywordObject
from powernad.Object.AdKeyword.ManagedKeywordObject import ManagedKeywordObject
class AdKeyword:

    def __init__(self, base_url, api_key, secret_key, customer_id):
        self.r = RestApi(base_url, api_key, secret_key, customer_id)

    def get_adkeyword_list_by_labelid(self, labelid):
        query = {'nccLabelId' : labelid}
        result = self.r.get('/ncc/keywords', query)

        adkeyword_list = []
        for arr in result:
            keyword = AdKeywordObject(arr)
            adkeyword_list.append(keyword)

        return adkeyword_list
    
    def get_adkeyword_list_by_ids(self, ids):
        
        query = {'ids' : ids}
        result = self.r.get('/ncc/keywords', query)

        adkeyword_list = []
        for arr in result:
            keyword = AdKeywordObject(arr)
            adkeyword_list.append(keyword)

        return adkeyword_list
        

    def get_adkeyword_list_by_groupid(self, nccAdgroupId= None, baseSearchId=None, recordSize = None, selector = None):

        query = {'nccAdgroupId' : nccAdgroupId, 'baseSearchId' : baseSearchId, 'recordSize' : recordSize, 'selector' : selector }
        result = self.r.get('/ncc/keywords', query)

        adkeyword_list = []
        for arr in result:
            keyword = AdKeywordObject(arr)
            adkeyword_list.append(keyword)

        return adkeyword_list

    
    def get_adkeyword(self, nccKeywordId):
        
        result = self.r.get('/ncc/keywords/'+ nccKeywordId)
        result = AdKeywordObject(result)

        return result

    def create_adkeyword(self, nccAdgroupId, CreateAdKeywordObject):
        data = jsonpickle.encode(CreateAdKeywordObject, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data =  [data]
        data_str = json.dumps(data)

        self.r.post('/ncc/keywords', data_str, {'nccAdgroupId' : nccAdgroupId})

    def update_adkeyrword(self, nccKeywordId, fields, UpdateAdKeywordObject):
        
        data = jsonpickle.encode(UpdateAdKeywordObject, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = json.dumps(data)

        query = {'fields' : fields}

        result = self.r.put('/ncc/keywords/'+nccKeywordId, data_str, query)
        result = AdKeywordObject(result)

        return result

    def delete_adkeyword(self, nccKeywordId):
        self.r.delete('/ncc/keywords/'+ nccKeywordId)
        return True

    def delete_adkeyword_many(self, ids_list):
        query = {'ids' : ids_list}
        self.r.delete('/ncc/keywords', query)

    def null_dict(self, input_dict):
        real = dict()
        for now in input_dict:
            if input_dict[now] != None:
                real.update({now :input_dict[now]})
        return real

    def managed_keyword_list(self, keywords):
        result = self.r.get('/ncc/managedKeyword', {'keywords' : keywords})

        managedkeyword_list = []
        for arr in result:
            managedkeyword = ManagedKeywordObject(arr)
            managedkeyword_list.append(managedkeyword)

        return managedkeyword_list


        pprint.pprint(result)



