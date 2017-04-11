import json
import jsonpickle
import pprint
from powernad.Connector.restapi import RestApi
from powernad.Object.Estimate.EstimateAvgObject import EstimateAvgObject
from powernad.Object.Estimate.EstimateMedianObject import EstimateMedianObject
from powernad.Object.Estimate.EstimateExposureMiniObject import EstimateExposureMiniObject
from powernad.Object.Estimate.EstimatePerformanceObject import EstimatePerformanceObject
from powernad.Object.Ad.AdObject import AdObject
class Estimate:
    def __init__(self, base_url, api_key, secret_key, customer_id):
        self.r = RestApi(base_url, api_key, secret_key, customer_id)

    def get_avg_position_bid_list(self, type, GetEstimateObject):
        
        data = jsonpickle.encode(GetEstimateObject, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = json.dumps(data)

        result = self.r.post('/estimate/average-position-bid/' + type, data_str)
        result = result['estimate']
        estimate_list = []
        for arr in result:
            print(arr)
            estimate = EstimateAvgObject(arr)
            estimate_list.append(estimate)

        return estimate_list

    def get_median_bid_list(self, type, GetMedianBidObject):
        data = jsonpickle.encode(GetMedianBidObject, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = json.dumps(data)

        result = self.r.post('/estimate/median-bid/' + type, data_str)
        result = result['estimate']
        estimate_list = []
        for arr in result:
            print(arr)
            estimate = EstimateMedianObject(arr)
            estimate_list.append(estimate)

        return estimate_list

    def get_exposure_mini_bid_list(self, type, GetExposureMiniBidObject):
        data = jsonpickle.encode(GetExposureMiniBidObject, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = json.dumps(data)

        result = self.r.post('/estimate/exposure-minimum-bid/' + type, data_str)
        result = result['estimate']
        estimate_list = []
        for arr in result:
            print(arr)
            estimate = EstimateExposureMiniObject(arr)
            estimate_list.append(estimate)

        return estimate_list

    def get_performance_list(self, type, GetPerformanceObject):
        data = jsonpickle.encode(GetPerformanceObject, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = json.dumps(data)

        result = self.r.post('/estimate/performance/' + type, data_str)
        result = result['estimate']
        
        estimate_list = []
        for arr in result:
            print(arr)
            estimate = EstimatePerformanceObject(arr)
            estimate_list.append(estimate)

        return estimate_list

    def get_performance_list_many(self, GetPerformanceObjectList):
        data = jsonpickle.encode(GetPerformanceObjectList, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = json.dumps(data)

        result = self.r.post('/estimate/performance/' + type, data_str)
        result = result['estimate']
        
        estimate_list = []
        for arr in result:
            print(arr)
            estimate = EstimatePerformanceObject(arr)
            estimate_list.append(estimate)

        return estimate_list
        

    def null_dict(self, input_dict):
        real = dict()
        for now in input_dict:
            if input_dict[now] != None:
                real.update({now :input_dict[now]})
        return real

