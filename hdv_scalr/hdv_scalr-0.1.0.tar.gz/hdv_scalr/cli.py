import argparse, os, pprint
from importlib.machinery import SourceFileLoader

from .api import Config, xml_to_dict, Scalr
from .utils import FarmList, ServerList, RoleList

def main():
    prs = argparse.ArgumentParser()
    prs.add_argument('--farm',  nargs=1, metavar='farm_name', default=None, const=None)
    prs.add_argument('--role',  nargs=1, metavar='role_alias', default=None, const=None)
    prs.add_argument('--alias', nargs=1, metavar='server_alias', default=None, const=None)
    output = prs.parse_args()
    return output

def runner(args):
    api = get_api()
    util = None
    args_list = (args.farm, args.role, args.alias)

    if (args_list[1] is None or args_list[1] == "") and args_list[2] is not None:
        raise Exception("--role cannot be empty")
    
#         utils = FarmList(api)
# 
#     if args.rolelist[0]:
#         utils = RoleList(args.rolelist[0])
        

    total_arg_count = len([a for a in args_list if a is not None])
    if   total_arg_count == 1:
        util = RoleList(api, farm_name=args_list[0][0])
    elif total_arg_count == 2:
        util = ServerList(api, farm_name=args_list[0][0], role_alias=args_list[1])
        pass
    elif total_arg_count == 3:
        pass
    else:
        util = FarmList(api) 
        
        
    pp = pprint.PrettyPrinter()
    if util is not None:
        pp.pprint(util.get_result())
    else:
        pass   
        
def get_api():
    cwd = os.getcwd()
    scalr_config = SourceFileLoader('scalr_config', cwd + '/scalr_config.py').load_module()
    
    config = Config()
    config.key_id = scalr_config.KEY_ID
    config.access_key = scalr_config.ACCESS_KEY
    config.output_formatter = xml_to_dict
    
    return Scalr(config)       