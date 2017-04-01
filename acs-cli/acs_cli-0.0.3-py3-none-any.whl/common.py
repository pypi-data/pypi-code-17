import base64
import requests


class APIBase(object):
    def __init__(self, base_url, api_collection, api, tenant='-default-', version=1):
        self.base_url = base_url
        self.api_collection = api_collection
        self.url = '{base_url}/api/{tenant}/public/{api_name}/versions/{version}'.\
            format(base_url=base_url, tenant=tenant, api_name=api_collection, version=version)
        self.api = api

    #def __getattr__(self, item):
    #    if item.startswith('get_'):
    #        return lambda ticket, entity_id: self.single_entity(item, ticket, entity_id)
    #    elif item.startswith('list_'):
    #        return lambda ticket, skip_count, max_items: self.list_collection(item, ticket, skip_count, max_items)

    def single_entity(self, ticket, path_template, path_params):
        #print('Handling get request:', path_template, path_params)
        headers = auth_header(ticket)
        path = path_template.format_map(vars(path_params))
        #print('Built path:', path)
        response = requests.get(self.url+path, headers=headers)
        # return response.json()['entry'] if response == 200 else response.json()['error']
        return response

    def list_collection(self, ticket, path_template, path_params, skip_count=0, max_items=10):
        #print('Handling list request: ', path_template, path_params)
        headers = auth_header(ticket)
        path = path_template.format_map(vars(path_params))
        response = requests.get(self.url+path, headers=headers, params={'skipCount': skip_count, 'maxItems': max_items})
        return response

    def path(self, path_within_api=''):
        return '/'.join([self.url, self.api, path_within_api])


def auth_header(ticket):
    # Avoid base64 encoding errors
    if ticket is None:
        ticket = ""
    base64_ticket = base64.b64encode(bytes(ticket, 'UTF-8')).decode("ISO-8859-1")
    return {'Authorization': 'Basic {0}'.format(base64_ticket)}

