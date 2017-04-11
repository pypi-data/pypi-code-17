import json
import jsonpickle
import pprint
from powernad.Connector.restapi import RestApi
from powernad.Object.ManagedCustomerLink.ManagedCustomerLinkObject import ManagedCustomerLinkObject

class ManagedCustomerLink:
    
    def __init__(self, base_url, api_key, secret_key, customer_id):
        self.r = RestApi(base_url, api_key, secret_key, customer_id)
    
    def get_managed_customer_link_list(self, rel_type= None):
        query = {'type' : rel_type}
        result = self.r.get('/customer-links', query)
        customer_list = []
        for arr in result:
            customer = ManagedCustomerLinkObject(arr)
            customer_list.append(customer)

        return customer_list

    