from .apibase import APIBase
class Application(APIBase):
    '''
    灵雀云应用
    '''
    
    _aliasmap = {
        'region_id': 'region',
        'name':'app_name',
    }
    
    _hideset = {'app_name', 'region'}
    
    @classmethod
    def create(cls, alauda, name, region_name = None, yml = None):
        url = '/v1/applications/{namespace}'
        data = {
           'app_name': name,
           'region': region_name if region_name else alauda.default_region,
           'namespace': alauda.namespace,
        }
        if yml:
            data['services'] = yml
            
        r = alauda._request_helper(url, 'post', data = data)
        
        if 201 == r.status_code:
            return cls(alauda, r.json())
        else:
            print(data)
            raise Exception('发生了异常：\n{}\n{}'.format(r.status_code, r.text))
            
    @classmethod
    def get(cls, alauda, name, region_name = None):
            
        url = '/v1/applications/{namespace}/{name}'.format(
            name = name, namespace = alauda.namespace)
        #region_name可以为空字符串。这代表使用系统提供的所有region。
        params = {'region': region_name if region_name != None else alauda.default_region}
        r = alauda._request_helper(url, 'get', params = params)
        
        if 200 == r.status_code:
            return cls(alauda, r.json())
        elif 404 == r.status_code:
            return None
        else:
            raise Exception('发生了异常：\n{}\n{}'.format(r.status_code, r.text))
    
    @classmethod
    def list(cls, alauda, region_name = None):
        '列出应用'
        url = '/v1/applications/{namespace}'
        #region_name可以为空字符串。这代表使用系统提供的所有region。
        params = {'region': region_name if region_name != None else alauda.default_region}
        r = alauda._request_helper(url, 'get', params = params)
        
        if 200 == r.status_code:
            ret = []
            for data in r.json():
                ret.append(cls(alauda, data))
            return ret
        else:
            print(url, params)
            raise Exception('发生了异常：\n{}\n{}'.format(r.status_code, r.text))
    
    def __init__(self, alauda, data):
        self._alauda = alauda
        super().__init__(data)
        
    @property
    def region(self):
        return self._alauda.get_region(self.region_id)
        
    @property
    def region_name(self):
        return self.region.name
    
    def _format_url(self, url = ''):
        return '/v1/applications/{namespace}/{name}/{url}?region={region}'.format(
            name = self.name, url = url, namespace = self._alauda.namespace, region = self.region_name)

    @property
    def api_url(self):
        return self._format_url()
        
    @property
    def yaml(self):
        url = self._format_url('/yaml')
        r = self._alauda._request_helper(url, 'get')
        if 200 == r.status_code:
            return r.text
        else:
            raise Exception('发生了异常：\n{}\n{}'.format(r.status_code, r.text))
            
    def update(self, yaml):
        files = {'services': yaml}
        r = self._alauda._request_helper(self.api_url, 'put', files = files)
        if 204 == r.status_code:
            return
        else:
            raise Exception('发生了异常：\n{}\n{}'.format(r.status_code, r.text))
            
    def list_service(self):
        return self.region.list_service(self.name)
        
    def delete_service(self, name):
        return self.region.delete_service(name, self.name)
        
    def get_service(self, name):
        return self.region.get_service(name, self.name)
            
            
    def start(self):
        url = self._format_url('/start')
        r = self._alauda._request_helper(url, 'put')
        if 204 == r.status_code:
            return r.text
        else:
            raise Exception('发生了异常：\n{}\n{}'.format(r.status_code, r.text))
            
    def stop(self):
        url = self._format_url('/start')
        r = self._alauda._request_helper(url, 'put')
        if 204 == r.status_code:
            return r.text
        else:
            raise Exception('发生了异常：\n{}\n{}'.format(r.status_code, r.text))
            
    def delete(self):
        r = self._alauda._request_helper(self.api_url, 'delete')
        if 204 == r.status_code:
            return r.text
        else:
            raise Exception('发生了异常：\n{}\n{}'.format(r.status_code, r.text))
            
    
    
    def __repr__(self):
        return '<Application [{}] in [{}], len[{}]>'.format(self.name, self.region_name, len(self.services))
