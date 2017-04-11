import json
import jsonpickle
import pprint
from powernad.Connector.restapi import RestApi
from powernad.Object.Stat.StatObject import StatObject

class Stat:
    def __init__(self, base_url, api_key, secret_key, customer_id):
        self.r = RestApi(base_url, api_key, secret_key, customer_id)

    def get_stat_by_id(self, id, fields, timeRange, dataPreset=None, timeIncrement= None, breakdown=None):
        query = {'id' : id, 'fields' : fields, 'timeRange' : timeRange, 'dataPreset' : dataPreset,
                     'timeIncrement' : timeIncrement, 'breakdown' : breakdown}
        result = self.r.get('/stats', query)
        result = StatObject(result)

        return result
        
    def get_stat_by_ids(self, ids, fields, timeRange, dataPreset=None, timeIncrement= None, breakdown=None):
        query = {'ids' : ids, 'fields' : fields, 'timeRange' : timeRange, 'dataPreset' : dataPreset,
                     'timeIncrement' : timeIncrement, 'breakdown' : breakdown}
        result = self.r.get('/stats', query)
        pprint.pprint(result)
        result = StatObject(result)

        return result

    def get_stat_by_type(self, id, statType):
        query = {'id' :id, 'statType' : statType}
        result = self.r.get('/stats', query)
        pprint.pprint(result)

