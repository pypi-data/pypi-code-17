from .apibase import APIBase, APISimpleDataBase
import yaml


class EndPoint(APIBase):
    
    _aliasmap = {
    }
    
    _hideset = {'protocol'}
    
    def __init__(self, data):
        super().__init__(data)
        
    @property
    def domain(self):
        return self._json_data.get('customer_domain') or self.default_domain
        
    @property
    def protocol(self):
        if self.endpoint_type == 'http-endpoint':
            return 'http'
        else:
            return self._json_data['protocol']
        
    @property
    def url(self):
        if self.endpoint_type == 'http-endpoint' and self.service_port == 80:
            return 'http://' + self.domain
            
        return '{}://{}:{}'.format(self.protocol, self.domain, self.service_port)
        
    def __repr__(self):
        return '<EndPoint {}>'.format(self.url)
    

def format_url(alauda, region_name, name, app_name, act = ''):
    url = '/v1/services/{namespace}/{name}/{act}?region_name={region_name}'.format(
        name = name, act = act, namespace = alauda.namespace,
        region_name = region_name if region_name != None else alauda.default_region,
        )
    if app_name is not None:
        url += '&application=' + app_name
    return url

class Service(APISimpleDataBase):
    '''
    灵雀云服务
    '''
    
    _aliasmap = {
        'name':'service_name',
        # 'app_name':'application',
        # 'region_name':['region', 'name']
    }
    
    _hideset = {'service_name', 'application', 'app_name'}
    
    @classmethod
    def create(cls, alauda, config):
        '根据配置文件创建服务'
        
        url = '/v1/services/{namespace}/'
        r = alauda._request_helper(url, 'post', data = config)
        
        if 204 == r.status_code:
            print('成功创建了服务')
            return cls(alauda, r.json())
        else:
            raise Exception('发生了异常：\n{}\n{}'.format(r.status_code, r.text))
            
    @classmethod
    def get_data(cls, alauda, name, app_name = None, region_name = None):
        url = format_url(alauda, region_name, name, app_name)
        r = alauda._request_helper(url, 'get')
        if 200 == r.status_code:
            return r.json()
        elif r.status_code in (403, 404):
            return None
        else:
            raise Exception('发生了异常：\n{}\n{}'.format(r.status_code, r.text))
            
    @classmethod
    def get(cls, alauda, name, app_name = None, region_name = None):
        data = cls.get_data(alauda, name, app_name, region_name)
        if data is None:
            return None
        return cls(alauda, data)
    
    @classmethod
    def list(cls, alauda, app_name = None, region_name = None):
        '''
        列出服务
        '''
        # 获取应用中的服务：
        if app_name:
            url = '/v1/applications/{namespace}/{app_name}?region_name={region_name}'.format(
                namespace = alauda.namespace,app_name = app_name, 
                region_name = region_name if region_name != None else alauda.default_region,
                )
            r = alauda._request_helper(url, 'get')
            if 200 == r.status_code:
                ret = []
                for data in r.json()['services']:
                    data['application'] = app_name
                    ret.append(cls(alauda, data, True))
                return ret
            else:
                raise Exception( '发生了异常：\n{}\n{}'.format(r.status_code, r.text))
        
        #获取不在应用中的服务：
        
        url = format_url(alauda, region_name, '|', None)
        url = url.replace('/|/', '/')
        r = alauda._request_helper(url, 'get')
        if 200 == r.status_code:
            ret = []
            for data in r.json()['results']:
                if data.get('application'): #公有区不带application参数会返回包括应用内服务的所有服务。在这里将其过滤。
                    continue 
                ret.append(cls(alauda, data, True))
            return ret
        else:
            raise Exception( '发生了异常：\n{}\n{}'.format(r.status_code, r.text))
    
    @staticmethod
    def start_service(alauda, name, app_name, region_name = None):
        url = format_url(alauda, region_name, name, app_name, 'start')
        r = alauda._request_helper(url, 'put')
        if 204 == r.status_code:
            return True
        elif 400 == r.status_code:
            return False
        else:
            raise Exception( '发生了异常：\n{}\n{}'.format(r.status_code, r.text))
            
    @staticmethod
    def stop_service(alauda, name, app_name, region_name = None):
        url = format_url(alauda, region_name, name, app_name, 'stop')
        r = alauda._request_helper(url, 'put')
        if 204 == r.status_code:
            return True
        elif 400 == r.status_code:
            return False
        else:
            raise Exception( '发生了异常：\n{}\n{}'.format(r.status_code, r.text))
            
    @staticmethod
    def delete_service(alauda, name, app_name, region_name = None):
        url = format_url(alauda, region_name, name, app_name)
        r = alauda._request_helper(url, 'delete')
        if 204 == r.status_code:
            return True
        else:
            raise Exception( '发生了异常：\n{}\n{}'.format(r.status_code, r.text))
            
    
    
    @staticmethod
    def yml_to_json(alauda, yml, region_name = None, application = None, run = False):
        '''
        将yaml格式的服务初始化参数转换为json格式。
        因为yaml可以包含多个服务描述，所以返回结果是一个包含数个json对象的数组。
        args:
            - yml yml对象，或者yml文本，或者打开的文件。
            - region_name 区域名
        returns:
            - json对象序列
        '''
        if not isinstance(yml,dict):
            yml = yaml.load(yml)
        print(yml)
        
        if region_name is None:
            region_name = alauda.default_region
        
        ret = []
        for (service_name,service_data) in yml.items():
            json = {
                'service_name':service_name,
                'namespace': alauda.namespace,
                'application': application,
                'region_name': region_name,
                
                'instance_ports': [],
                'volumes': [],
                'instance_envvars': {},
                
                # 'scaling_mode': 'MANUAL',
                # 'autoscaling_config': {
                #     'metric_name' : 'CPU_UTILIZATION',
                #     'metric_stat' : 'MEAN',
                #     'upper_threshold' : '0.6',
                #     'lower_threshold' : '0.1',
                #     'decrease_delta' : '1',
                #     'increase_delta' : '1',
                #     'minimum_num_instances' : '1',
                #     'maximum_num_instances' : '6',
                #     'wait_period' : '30'
                # },
                }
            ret.append(json)
            
            if run:
                json['target_state'] = 'STARTED'
            else:
                json['target_state'] = 'STOPPED'
                
                
            if 'image' in service_data:
                temp = (service_data['image'] + ':latest').split(':')
                json['image_name'] = temp[0]
                json['image_tag'] = temp[1]
                del service_data['image']
                
            if 'command' in service_data:
                json['run_command'] = service_data['command']
                del service_data['command']
            
            if 'links' in service_data:
                temp = {}
                json['linked_to_apps'] = temp
                for l in service_data['links']:
                    l = l.split(':')
                    if len(l) == 2:
                        temp[l[0]] = l[1]
                    else:
                        temp[l[0]] = l[0]
                del service_data['links']
                
            if 'size' in service_data:
                json['instance_size'] = service_data['size']
                del service_data['size']
                
            if 'number' in service_data:
                json['target_num_instances'] = service_data['number']
                del service_data['number']
            
            if 'ports' in service_data:
                for p in service_data['ports']:
                    p = p.split('/')
                    container_port = p[0]
                    protocol = 'tcp'
                    if 2 == len(p):
                        protocol = p[1]
                    else:
                        if 80 == container_port or 8080 == container_port:
                            protocol == 'http'
                    temp = {
                        'container_port':container_port,
                        'protocol': protocol
                        }
                    if 'http' == protocol:
                        temp['endpoint_type'] = 'http-endpoint'
                    elif 'tcp' == protocol:
                        temp['endpoint_type'] = 'tcp-endpoint'
                    else:
                        raise Exception('指定了不支持的端口协议：{}'.format(protocol))
                    json['instance_ports'].append(temp)
                    
                del service_data['ports']
            
            if 'expose' in service_data:
                for p in service_data['expose']:
                    json['instance_ports'].append({
                            'container_port': p,
                            'protocol': 'tcp',
                            'endpoint_type': 'internal-endpoint'
                        })
                del service_data['expose']
            
            if 'volumes' in service_data:
                for v in service_data['volumes']:
                    v = (v + ':10').split(':')
                    json['volumes'].append({
                        'app_volume_dir' : v[0],
                        'volume_type' : 'EBS',
                        'size_gb' : v[1],
                        })
                del service_data['volumes']
                
            if 'environment' in service_data:
                envs = service_data['environment']
                if isinstance(envs, list):
                    for env in envs:
                        env = env.split('=')
                        if 1 == len(env):
                            json['instance_envvars'][env[0]] = None
                        else:
                            json['instance_envvars'][env[0]] = env[1]
                else:
                    for (k, v) in envs.items():
                        json['instance_envvars'][k] = v
                        
                del service_data['environment']
                
            if len(service_data.items()) > 0:
                print('无法处理的参数:\n{}'.format(service_data))
        
        return ret
    
    def __init__(self, alauda, data, is_simple = False):
        self._alauda = alauda
        self._endpoints = None
        super().__init__(data, is_simple)
        
    def list_endpoint(self):
        if not self._endpoints:
            self._endpoints = []
            if 'alauda_load_balancer' in self._json_data:
                for data in self._json_data['alauda_load_balancer'].get('endpoints', []):
                    self._endpoints.append(EndPoint(data))
            else:
                if 'instance_ports' not in self._json_data:
                    self._update_to_full()
                for data in self._json_data.get('instance_ports', []):
                    self._endpoints.append(EndPoint(data))
        return self._endpoints
        
    @property
    def app_name(self):
        return self._json_data.get('application')
        
    @property
    def region_name(self):
        region_id = self._json_data.get('region_id')
        if region_id:
            return self._alauda.get_region(region_id).name
        else:
            return self._json_data['region']['name']
        
    def _get_full(self):
        return self.get_data(self._alauda, self.name, self.app_name, self.region_name)
    
    def _format_url(self, url = ''):
        return format_url(self._alauda, self.region_name, self.name, self.app_name, url)
        
    @property
    def api_url(self):
        return self._format_url()
            
    def start(self):
        '启动此服务'
        return self.start_service(self._alauda, self.name, self.app_name)
    
    def stop(self):
        '停止此服务'
        return self.stop_service(self._alauda, self.name, self.app_name)
            
    def delete(self):
        '删除此服务'
        return self.delete_service(self._alauda, self.name, self.app_name)
            
    def update(self, name = None, target_num_instances = None, \
    image_tag = None, scaling_mode = None):
        '更新服务参数'
        data = {
            'service_name':name or self.name,
            'target_num_instances': target_num_instances or self.target_num_instances,
            'image_tag': image_tag or self.image_tag,
            'scaling_mode': scaling_mode or self.scaling_mode
        }
        r = self._alauda._request_helper(self.api_url, 'put', data)
        if 204 == r.status_code:
            return True
        else:
            raise Exception( '发生了异常：\n{}\n{}'.format(r.status_code, r.text))
    
    def __repr__(self):
        if self.app_name is None:
            return '<Service [{}] in [{}]>'.format(self.name, self.region_name)
        else:
            return '<Service [{}] of [{}] in [{}]>'.format(self.name, self.app_name, self.region_name)