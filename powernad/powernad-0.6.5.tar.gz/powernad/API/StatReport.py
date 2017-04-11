import json
import jsonpickle
import pprint
from powernad.Connector.restapi import RestApi
from powernad.Object.StatReport.StatReportObject import StatReportObject

class StatReport: #대용량 보고서
     
    def __init__(self, base_url, api_key, secret_key, customer_id):
        self.r = RestApi(base_url, api_key, secret_key, customer_id)

    def get_stat_report_list(self):
        result = self.r.get('/stat-reports')
        stat_list = []
        for arr in result:
            stat = StatReportObject(arr)
            stat_list.append(stat)

        return stat_list

    def get_stat_report(self, reportJobId):
        result = self.r.get('/stat-reports/' + reportJobId)
        result = StatReportObject(result)
        
        return result

    def create_stat_report(self, CreateStatReportObject):
        
        data = jsonpickle.encode(CreateStatReportObject, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = json.dumps(data)

        result = self.r.post('/stat-reports', data_str)
        result = StatReportObject(result)

        return result

    def delete_stat_reports(self, reportJobId):
        self.r.delete('/stat-reports/'+ reportJobId)
        return True

    def null_dict(self, input_dict):
        real = dict()
        for now in input_dict:
            if input_dict[now] != None:
                real.update({now :input_dict[now]})
        return real
