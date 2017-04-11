import json
import jsonpickle
import pprint
from powernad.Connector.restapi import RestApi
from powernad.Object.RelKwdStat.RelKwdStatObject import RelKwdStatObject
class RelKwdStat:
    
    def __init__(self, base_url, api_key, secret_key, customer_id):
        self.r = RestApi(base_url, api_key, secret_key, customer_id)

    def get_relkwd_stat_list(self, siteId, biztpId=None, hintKeywords=None, includeHintKeywords=None, event=None, month= None, showDetail= None):
        query = {'siteId' : siteId, 'biztpId' : biztpId, 'hintKeywords' : hintKeywords,
         'includeHintKeywords' : includeHintKeywords, 'event' : event, 'month' : month, 'showDetail' : showDetail}
        result = self.r.get('/keywordstool', query)
        result = result['keywordList']
        relstat_list = []

        for arr in result:
            relstat = RelKwdStatObject(arr)
            relstat_list.append(relstat)

        return relstat_list
