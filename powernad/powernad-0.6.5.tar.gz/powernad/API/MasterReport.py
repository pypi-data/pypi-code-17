import json
import jsonpickle
import pprint
from powernad.Connector.restapi import RestApi
from powernad.Object.MasterReport.MasterReportObject import MasterReportObject

class MasterReport: #광고정보일괄다운로드탭
    def __init__(self, base_url, api_key, secret_key, customer_id):
        self.r = RestApi(base_url, api_key, secret_key, customer_id)

    def get_master_report_list(self):
        result = self.r.get('/master-reports')
        
        mreport_list = []
        for arr in result:
            mreport = MasterReportObject(arr)
            mreport_list.append(mreport)

        return mreport_list

    def get_master_report_by_id(self, id):
        result = self.r.get('/master-reports/'+ id)
        
        result = MasterReportObject(result)
        return result

    def create_master_report(self, CreateMasterReportObject):
        data = jsonpickle.encode(CreateMasterReportObject, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = json.dumps(data)

        result = self.r.post('/master-reports', data_str)
        result = MasterReportObject(result)

        return result

    def delete_master_report_all(self):
        self.r.delete('/master-reports')
        return True

    def delete_master_report_by_id(self, id):
        self.r.delete('/master-reports', {'id' : id})
        return True

    def null_dict(self, input_dict):
        real = dict()
        for now in input_dict:
            if input_dict[now] != None:
                real.update({now :input_dict[now]})
        return real
    
        
