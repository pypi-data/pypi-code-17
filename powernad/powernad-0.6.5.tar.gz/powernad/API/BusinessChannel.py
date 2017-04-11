import json
import jsonpickle
import pprint
from powernad.Connector.restapi import RestApi
from powernad.Object.BusinessChannel.BusinessChannelObject import BusinessChannelObject

class BusinessChannel:
    def __init__(self, base_url, api_key, secret_key, customer_id):
        self.r = RestApi(base_url, api_key, secret_key, customer_id)

    def get_business_channel_list(self):
        result = self.r.get('/ncc/channels')

        business_channel_list = []
        for arr in result:
            channel = BusinessChannelObject(arr)
            business_channel_list.append(channel)

        return business_channel_list
    
    def get_business_channel_list_by_type(self, tp):
        result = self.r.get('/ncc/channels',{'channelTp' : tp})

        business_channel_list = []
        for arr in result:
            channel = BusinessChannelObject(arr)
            business_channel_list.append(channel)

        return business_channel_list

    def get_business_channel_list_by_ids(self, ids):
        result = self.r.get('/ncc/channels',{'ids' : ids})

        business_channel_list = []
        for arr in result:
            channel = BusinessChannelObject(arr)
            business_channel_list.append(channel)
        return business_channel_list

    def get_business_channel(self, businessChannelId):
        
        result = self.r.get('/ncc/channels/'+businessChannelId)
        pprint.pprint(result)
        result = BusinessChannelObject(result)

        return result

    def create_business_channel(self, CreateBusinessChannelObj):
        
        data = jsonpickle.encode(CreateBusinessChannelObj, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = json.dumps(data)
        result = self.r.post('/ncc/channels', data_str)
        result = BusinessChannelObject(result)
        return result

    def update_business_channel(self, fields, CreateBusinessChannelObj):
        data = jsonpickle.encode(CreateBusinessChannelObj, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = json.dumps(data)
        result = self.r.put('/ncc/channels', data_str, fields)
        result = BusinessChannelObject(result)
        return result

    def delete_business_channel(self, businessChannelId):
        self.r.delete('/ncc/channels/'+businessChannelId)
        return True

    def delete_business_channel_by_ids(self, ids):
        self.r.delete('/ncc/channels', {'ids' : ids})
        return True
        
    def null_dict(self, input_dict):
        real = dict()
        for now in input_dict:
            if input_dict[now] != None:
                real.update({now :input_dict[now]})
        return real