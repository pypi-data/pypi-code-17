def farm_details(scalr, farm_name=None, farm_id=None):
    if (farm_id is None) :
        farms = scalr.read()['FarmsListResponse']['FarmSet']['Item']
        for i in farms:
            if (i['Name'] == farm_name) :
                farm_id = i['ID']
     
    return scalr.set_action('FarmGetDetails', FarmID=farm_id).read()

class Util():
    def __init__(self, scalr, farm_name=None, farm_id=None):
        self.scalr = scalr
        self.farm_name = farm_name
        self.farm_id = farm_id
    
    def farm_details(self):
        farm = farm_details(self.scalr, self.farm_name, self.farm_id)
        if ('Error' in farm) :
            raise RuntimeError(farm['Error']['Message'])
        return farm
    
class FarmList(Util):
    
    def get_result(self):
        return self.scalr.read()['FarmsListResponse']['FarmSet']['Item']
    
class RoleList(Util):
    
    def get_result(self):
        roles = self.farm_details()['FarmGetDetailsResponse']['FarmRoleSet']['Item']
        output = {}
        for role in roles:
            output[role['Alias']]= role['Name']
        return output
    
class DBList(Util):
    
    def get_result(self):
        roles = self.farm_details()['FarmGetDetailsResponse']['FarmRoleSet']['Item']['ServerSet']['Item']
        output = {}
        for role in roles:
            converted = dict(role)
            if converted['IsDbMaster'] == '1':
                output['master'] = converted['ExternalIP']
            else:
                output['slave'] = converted['ExternalIP']
        
        return output
            
    def get_slave(self):
        result = self.get_result()
        return result['slave']
        
    
    def get_master(self):
        result = self.get_result()
        return result['master']
            
        
    
    
class ServerList(Util):
    
    def __init__(self, scalr, farm_name=None, role_alias=None):
        self.role_alias = role_alias
        super().__init__(scalr, farm_name)

    def get_result(self):
        roles = self.farm_details()['FarmGetDetailsResponse']['FarmRoleSet']['Item']
        output = []
        for role in roles:
            if role['Alias'] != self.role_alias:
                continue
            if isinstance(role['ServerSet']['Item'], list):
                for server in role['ServerSet']['Item']:
                    output+= [v for k, v in server.items() if k == 'PublicIP']
            else :
                output = [role['ServerSet']['Item']['PublicIP']]
        return output