import base64
import requests
import json

version = '0.0.8'


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

    def common_query_params(self, args):
        args_dict = vars(args)
        common = {
            'fields': args_dict.get('fields'),
            'include': args_dict.get('include'),
            'where': args_dict.get('where')
        }
        return common

    def single_entity(self, ticket, path_template, args):
        #print('Handling get request:', path_template, path_params)
        headers = auth_header(ticket)
        path = path_template.format_map(vars(args))
        #print('Built path:', path)
        response = requests.get(self.url+path, headers=headers, params=self.common_query_params(args))
        # return response.json()['entry'] if response == 200 else response.json()['error']
        return response

    def list_collection(self, ticket, path_template, args, skip_count=0, max_items=10):
        #print('Handling list request: ', path_template, path_params)
        headers = auth_header(ticket)
        path = path_template.format_map(vars(args))
        params = {'skipCount': skip_count, 'maxItems': max_items}
        params.update(self.common_query_params(args))
        response = requests.get(self.url+path, headers=headers, params=params)
        return response

    def create_entity(self, ticket, path_template, args, required_param_names, optional_param_names=[]):
        json_params = args.json_data
        args_as_dict = vars(args)
        entity = json.loads(json_params) if json_params is not None else dict()
        for param in required_param_names+optional_param_names:
            if args_as_dict.get(param) and entity.get(param):
                raise ValueError('Parameter {} supplied in both JSON and named arguments'.format(param))
            elif args_as_dict.get(param):
                entity[param] = args_as_dict[param]

        # Check that after the merge of json-data and named args, we have all the mandatory fields
        for param in required_param_names:
            if param not in entity or entity[param] is None:
                raise ValueError('Missing mandatory parameter "{}"'.format(param))

        headers = auth_header(ticket)
        path = path_template.format_map(args_as_dict)
        # TODO: bug where --json-data and --content=<filepath> do not mix well
        if args_as_dict.get('content'):
            files = {'filedata': args.content}
            response = requests.post(self.url+path, data=entity, files=files, headers=headers)
        else:
            response = requests.post(self.url+path, json=entity, headers=headers)
        return response

    def update_entity(self, ticket, path_template, args, required_param_names, optional_param_names):
        json_params = args.json_data
        args_as_dict = vars(args)
        entity = json.loads(json_params) if json_params is not None else dict()
        # TODO: factor out param validation etc.
        for param in required_param_names+optional_param_names:
            if args_as_dict.get(param) and entity.get(param):
                raise ValueError('Parameter {} supplied in both JSON and named arguments'.format(param))
            elif args_as_dict.get(param):
                entity[param] = args_as_dict[param]

        # Check that after the merge of json-data and named args, we have all the mandatory fields
        for param in required_param_names:
            if param not in entity or entity[param] is None:
                raise ValueError('Missing mandatory parameter "{}"'.format(param))

        headers = auth_header(ticket)
        path = path_template.format_map(args_as_dict)
        response = requests.put(self.url+path, json=entity, headers=headers)
        return response

    def delete_entity(self, ticket, path_template, path_params):
        headers = auth_header(ticket)
        path = path_template.format_map(vars(path_params))
        response = requests.delete(self.url+path, headers=headers)
        return response

    def upload_content(self, ticket, path_template, args, required_param_names):
        headers = auth_header(ticket)
        path = path_template.format_map(vars(args))
        # Hmmm, I appear to have hardcoded the 'content' parameter here.
        # Have I accidentally done similar stuff elsewhere?
        response = requests.put(self.url+path, data=args.content, headers=headers)
        return response

    def path(self, path_within_api=None):
        elements = [self.url, self.api]
        if path_within_api is not None:
            elements.append(path_within_api)
        return '/'.join(elements)


class Nodes(APIBase):
    def __init__(self, base_url):
        # alfresco = 'core' API
        APIBase.__init__(self, base_url, 'alfresco', 'nodes')

def auth_header(ticket):
    # Avoid base64 encoding errors
    if ticket is None:
        ticket = ""
    base64_ticket = base64.b64encode(bytes(ticket, 'UTF-8')).decode("ISO-8859-1")
    return {'Authorization': 'Basic {0}'.format(base64_ticket)}

