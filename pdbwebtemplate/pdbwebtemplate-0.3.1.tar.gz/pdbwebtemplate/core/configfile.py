import ConfigParser
import ast
import logging

class ConfigFile(object):
    
    __config = None
          
    def __init__(self):
        self.__config = ConfigParser.ConfigParser()
        file_name = 'mypromo/settings.ini'
        self.__config.read(file_name)
        
    def get_config_variable(self, section, param, type_var=None, raise_except=True):
        try:          
            value = self.__config.get(section, param, type_var)
            if type_var == 'array':
                value = ast.literal_eval(value)
            if type_var == 'integer':
                value = int(value)    
                
            return value    
        except Exception as e:
            if raise_except:
                logging.critical('Error getting config variable in section: {}, param: {}, type_var: {}'.
                                 format(section, param, type_var))
                raise e