import datetime
import base64
import hmac
import hashlib
import requests

class Config():
    
    def __init__(self):
        
        self.key_id = None
        self.access_key = None
        self.endpoint = 'https://api.scalr.net/'
        self.version = '2.3.0'
        self.auth_version = '3'
        self.action = 'FarmsList'
        
        self.output_formatter = None
        
class Scalr():
    
    def __init__(self, config):
        
        self.config = config
        self.print_config_params = False
        self.action_params = {}
        
    def read(self):
        
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        params = {
            "Action": self.config.action,
            "Version": self.config.version,
            "AuthVersion": self.config.auth_version,
            "Timestamp": timestamp,
            "KeyID": self.config.key_id,
            "Signature":  base64.b64encode(hmac.new(str.encode(self.config.access_key), str.encode(":".join([self.config.action, self.config.key_id, timestamp])), hashlib.sha256).digest()),
        }
        params.update(self.action_params)
        
        if self.print_config_params == True:
            return params
        
        result = requests.get(self.config.endpoint, params)
        
        #default output is raw string
        if self.config.output_formatter is None :
            return result.text
        
        return self.config.output_formatter(result)
    
    def set_action(self, action, **kargs):
        self.config.action = action
        self.action_params = kargs
        return self
    
    def __str__(self):
        self.print_config_params = True
        params = str(self.read())
        self.print_config_params = False
        return params
        
 
def xml_to_dict(result):   
    import xmltodict
    return xmltodict.parse(result.text)
