from .apibase import APIBase
from .service import Service
from .application import Application


class Node(APIBase):
        
    def __repr__(self):
        if 'total_cpus' in self.resources:
            return '<Node {}: {} ({}core/{})>'.format(self.type, self.private_ip, self.resources['total_cpus'], self.resources['total_mem'])
        else:
            return '<Node {}: {}>'.format(self.type, self.private_ip)
    
    @property
    def is_slave(self):
        return self.type == 'SLAVE'
            
class Region(APIBase):
    '''
    可用区
    单个账号中有多个可用区，一些是系统提供的可用区，一些是私有区。
    可用区影响服务和应用的可见性。镜像仓库和构建不受可用区影响。
    '''
    
    
    @classmethod
    def list(cls, alauda):
        '列出应用'
        url = '/v1/regions/{namespace}'
        r = alauda._request_helper(url, 'get')
        
        if 200 == r.status_code:
            ret = []
            for data in r.json():
                ret.append(cls(alauda, data))
            return ret
        else:
            raise Exception('发生了异常：\n{}\n{}'.format(r.status_code, r.text))
       
    
    _aliasmap = {
    }
    
    _hideset = {}
    
    def __init__(self, alauda, data):
        self._alauda = alauda
        super().__init__(data)
        
    def __repr__(self):
        return '<Region {}:{} [{}]>'.format(self.name, self.display_name, self.id)
        
    def list_node(self):
        url = '/v1/regions/{{namespace}}/{region_name}/nodes'.format(region_name = self.name)
        r = self._alauda._request_helper(url, 'get')
        if 200 == r.status_code:
            ret = []
            for data in r.json():
                ret.append(Node(data))
            return ret
        else:
            raise Exception( '发生了异常：\n{}\n{}'.format(r.status_code, r.text))
        
    def create_service(self, config):
        return Service.create(self._alauda, config)
        
    def get_service(self, name, app_name = None):
        return Service.get(self._alauda, name, app_name, self.name)
    
    def list_service(self, app_name = None):
        return Service.list(self._alauda, app_name, self.name)
        
    def delete_service(self, name, app_name = None):
        return Service.delete_service(self._alauda, name, app_name, self.name)
        
    def create_application(self, name, yml = None):
        return Application.create(self._alauda, name, self.name, yml)
        
    def get_application(self, name):
        return Application.get(self._alauda, name, self.name)
        
    def list_application(self):
        return Application.list(self._alauda, self.name)
