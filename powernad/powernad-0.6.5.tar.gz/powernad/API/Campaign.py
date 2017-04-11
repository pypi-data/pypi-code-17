# pylint: disable=C0103
# pylint: disable=E0401


from powernad.Connector.restapi import RestApi
from powernad.Object.Campaign.CampaignObject import CampaignObject
import json
import jsonpickle
import pprint

class Campaign:
    def __init__(self, base_url, api_key, secret_key, customer_id):
        self.r = RestApi(base_url, api_key, secret_key, customer_id)


    def get_campaign_list(self, campaignType=None, baseSearchId=None, recordSize=None, selector=None):
        
        query = {'campaignType' : campaignType, 'baseSearchId' : baseSearchId, 'recordSize' : recordSize, 'selector' : selector}
        result = self.r.get('/ncc/campaigns', query)

        camp_list = []
        for arr in result:
            print(arr)
            camp = CampaignObject(arr)
            camp_list.append(camp)

        return camp_list

    def get_campaign_list_by_ids(self, ids):
        query = {'ids' : ids}

        result = self.r.get('/ncc/campaigns', query)
        
        camp_list = []
        for arr in result:
            print(arr)
            camp = CampaignObject(arr)
            camp_list.append(camp)

        return camp_list

    def get_campaign(self, campaignId):
        query = {'campaignId' : campaignId}
        result = self.r.get('/ncc/campaigns', query)
        camp = CampaignObject(result)
        return camp

    def create_campaign(self, campaign_add_object):
        
        data = jsonpickle.encode(campaign_add_object, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = json.dumps(data)
        
        
        self.r.post('/ncc/campaigns', data_str)

    def update_campaign(self, campaign_update_object, campaign_id, fields):
        data = jsonpickle.encode(campaign_update_object, unpicklable=False)
        result = self.r.put('/ncc/campaigns/'+str(campaign_id), data, {'fields': fields}) #userLock, budget, period
        camp = CampaignObject(result)
        return camp


    def null_dict(self, input_dict):
        real = dict()
        for now in input_dict:
            if input_dict[now] != None:
                real.update({now :input_dict[now]})
        return real

