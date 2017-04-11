import json
import jsonpickle
import pprint
from powernad.Connector.restapi import RestApi

from powernad.Object.Label.LabelObject import LabelObject
from powernad.Object.Label.LabelRefObject import LabelRefObject

class Label: #즐겨찾기
    def __init__(self, base_url, api_key, secret_key, customer_id):
        self.r = RestApi(base_url, api_key, secret_key, customer_id)

    def get_label_list(self):
        result = self.r.get('/ncc/labels')

        label_list = []
        for arr in result:
            label = LabelObject(arr)
            label_list.append(label)

        return label_list

    def update_label(self, UpdateLabelObject):
        data = jsonpickle.encode(UpdateLabelObject, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data_str = json.dumps(data)

        result = self.r.put('/ncc/labels', data_str)
        
        result = LabelObject(result)

        return result

    def update_label_ref(self, UpdateLabelRefObject):
        data = jsonpickle.encode(UpdateLabelRefObject, unpicklable=False)
        data = json.loads(data)       
        data = self.null_dict(data)
        data = [data]
        data_str = json.dumps(data)

        result = self.r.put('/ncc/label-refs/', data_str)

        labelref_list = []
        for arr in result:
            labelref = LabelRefObject(arr)
            labelref_list.append(labelref)

        return labelref_list


    def null_dict(self, input_dict):
        real = dict()
        for now in input_dict:
            if input_dict[now] != None:
                real.update({now :input_dict[now]})
        return real
