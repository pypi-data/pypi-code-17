# pylint: disable=C0103
# pylint: disable=E0401


from powernad.Connector.restapi import RestApi
from powernad.Object.AdGroup.RestrictedKeyword import RestrictedKeyword
from powernad.Object.AdGroup.AdgroupObject import AdgroupObject
from powernad.Object.AdGroup.sub.target import target
from powernad.Object.AdGroup.sub.targetSummaryObject import targetSummaryObject
from powernad.Object.AdGroup.sub.adgroupAttrJson import adgroupAttrObject
from powernad.Object.AdGroup.AdgroupObject import AdgroupObject
import json
import jsonpickle
import pprint

class AdGroup:
    def __init__(self, base_url, api_key, secret_key, customer_id):
        self.r = RestApi(base_url, api_key, secret_key, customer_id)
    
    def get_restricted_keyword(self, adgroup_id):
        query = {'type': 'KEYWORD_PLUS_RESTRICT'}
        result = self.r.get('/ncc/adgroups/'+adgroup_id+"/restricted-keywords", query);
        restricted_list = []
        for arr in result:
            camp = RestrictedKeyword(arr)
            restricted_list.append(camp)

        return restricted_list
    
    def get_adgroup_list(self, campaignid = None, baseid = None, record_size = None, selector = None):
        query = {'nccCampaignId' : campaignid, 'baseSearchId' : baseid,
                 'record_size': record_size, 'selector' : selector}
        result = self.r.get('/ncc/adgroups', query)
        
        adgroup_list = []
        for arr in result:
            camp = AdgroupObject(arr)
            adgroup_list.append(camp)

        return adgroup_list
    
    def get_adgroup_list_by_ids(self, ids):
        query = {'ids' : ids}
        result = self.r.get('/ncc/adgroups', query)
        adgroup_list = []
        for arr in result:
            camp = AdgroupObject(arr)
            adgroup_list.append(camp)

        return adgroup_list

    def get_adgroup_by_adgroupid(self, adgroupId):
        result = self.r.get('/ncc/adgroups/'+adgroupId)
        adgroup = AdgroupObject(result)
        return adgroup

    def create_restricted_keyword(self, adgroup_id, restricted_keywords_object):
        data = jsonpickle.encode(restricted_keywords_object, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = [data]
        data_str = json.dumps(data_str);
        result = self.r.post('/ncc/adgroups/%s/restricted-keywords' % str(adgroup_id), data_str)

    def create_adgroup(self, create_adgroup_object):
        data = jsonpickle.encode(create_adgroup_object, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = json.dumps(data)
        result = self.r.post('/ncc/adgroups', data_str)
        result = AdgroupObject(result)
        return result
    
    def update_adgroup(self, adgroup_id, fields, UpdateAdgroupObject ):
        
        query = {'fields' : fields }
        data = jsonpickle.encode(UpdateAdgroupObject, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = json.dumps(data)
        result = self.r.put('/ncc/adgroups/'+adgroup_id,data_str, fields)
        result = AdgroupObject(result)
        return result
    
    def update_adgroup_entire(self, adgroup_id, UpdateEntireAdgroupObject):
        data = jsonpickle.encode(UpdateEntireAdgroupObject, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = json.dumps(data)
        result = self.r.put('/ncc/adgroups/'+adgroup_id, data)
        pprint.pprint(result)

    def delete_group_restricted_keyword(self, adgroup_id, res_keyword_id):
        result = self.r.delete('/ncc/adgroups/%s/restricted-keywords' % str(adgroup_id), {'ids' : res_keyword_id})
        return True

    def delete_adgroup(self, adgroup_id):
        result = self.r.delete('/ncc/adgroups/'+adgroup_id)
        return True
        


    def null_dict(self, input_dict):
        real = dict()
        for now in input_dict:
            if input_dict[now] != None:
                real.update({now :input_dict[now]})
        return real

