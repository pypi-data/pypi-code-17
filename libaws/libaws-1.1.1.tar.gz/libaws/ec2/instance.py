import argparse
import os
import threading,time
from libaws.common.logger import logger,enable_debug_log
from libaws.common.boto import *
from adapter import *
import vpc 
from libaws.base import utils as baseutils
from libaws.common import config,utils
from libaws.common.db import Ec2InstanceDb

instance_db = Ec2InstanceDb.get_db()

def create_key_pair(key,delete_exists=False,path="."):

    def save_key_pair_file(pem_file_path,key_content):

        if os.path.exists(pem_file_path):
            os.remove(pem_file_path)
        with open(pem_file_path,"w") as f:
            f.write(key_content)

    path = os.path.abspath(path)
    if not os.path.exists(path):
        baseutils.mkdirs(path)

    if delete_exists:
        client_ec2.delete_key_pair(KeyName=key)

    response = client_ec2.create_key_pair(KeyName=key)
    pem_file_name = key + "." + "pem"
    pem_file_path = os.path.join(path,pem_file_name)

    save_key_pair_file(pem_file_path,response['KeyMaterial'])
    if path != ".":
        back_pem_file_path = os.path.join('.',pem_file_name)
        save_key_pair_file(back_pem_file_path,response['KeyMaterial'])
        os.popen('chmod 400 %s' % (back_pem_file_path))

    os.popen('chmod 400 %s' % (pem_file_path))
    return pem_file_path 

def get_key_pair(d):

    if not d.has_key('keypair'):
        return None,None

    keypair = d['keypair']
    keyname = keypair['key'] 
    path = "."
    delete_exists = False
    if keypair.has_key('path'):
        path = keypair['path']
    
    path = get_convert_default_data_path(path)
    if keypair.has_key('delete_exists'):
        delete_exists = bool(keypair['delete_exists'])
    
    pem_file_path = create_key_pair(keyname,delete_exists,path)
    logger.info("create key %s key file %s success",keyname,pem_file_path)
    return keyname,pem_file_path

def create_vpc(d):

    if not d.has_key('vpc'):
        return True
    params = d['vpc']

    vpc_config_file = params['from_config']
    vpc_config_file = get_convert_default_data_path(vpc_config_file)
    vpc_data_name = None

    if params.has_key('name'):
        return vpc.create_one_vpc_from_config(vpc_config_file,params['name'])
    else:
        return vpc.create_default_vpc_from_config(vpc_config_file)

def get_volumes(d):
    if not d.has_key('volumes'):
        return None
    volumes = d['volumes']
    volume_list = []
    for volume in volumes: 
        size = int(volume['volume']['size'])
        name = volume['volume']['name']
        ebs = {}
        ebs_volume= {}
        ebs_volume['VolumeSize'] = size
        if volume.has_key('type'):
            ebs_volume['VolumeType'] = volume['volume']['type']

        ebs['Ebs'] = ebs_volume
        ebs['DeviceName'] = name 
        volume_list.append(ebs)
    
    device_maps = {
            'BlockDeviceMappings':volume_list
    }
    return device_maps


def get_attach_volumes(params):

    volumes = get_value(params,'volumes')
    if volumes is None:
        return []
    return volumes

def get_place_group(params):

    placegroup = get_value(params,'placegroup')
    if placegroup is None:
        return None

    return {'Placement':{'GroupName':placegroup}}

def get_vpc_id(subnet_id):

    try:
        subnet = ec2.Subnet(subnet_id)
        return subnet.vpc_id
    except Exception,e:
        logger.error("%s",e)
        return None


def monitor_spot_requests(spot_request_id_list,tags,pem_file_path,vpc_id):

    global instance_db
    tag_name = "" 
    while True:
        if 0 == len(spot_request_id_list):
            break
        try:
            req = client_ec2.describe_spot_instance_requests(SpotInstanceRequestIds = spot_request_id_list)
            spot_instance_requests = req['SpotInstanceRequests']

            completed_request_index_list = []
            for spot_instance_request in spot_instance_requests:
                spot_instance_request_id = spot_instance_request['SpotInstanceRequestId']
                logger.debug("spot instance request %s state %s",spot_instance_request_id,spot_instance_request['State'])
                if spot_instance_request['State'] == 'active':
                    instance_id = spot_instance_request['InstanceId']
                    launch_specification = spot_instance_request['LaunchSpecification']
                    if len(tags) > 0:
                        create_instance_tags([instance_id],tags)
                        tag_name = tags[0]['Value']
                    logger.info("spot instance request %s has been fullfilled to instance %s",spot_instance_request_id,instance_id)
                    image_id = launch_specification['ImageId']
                    key_name = launch_specification['KeyName']
                    security_group_id = launch_specification['SecurityGroups'][0]['GroupId']  
                    subnet_id = launch_specification['SubnetId']
                    instance_type = launch_specification['InstanceType']
                    instance_db.save_instance_info(instance_id,tag_name,image_id,key_name,security_group_id,subnet_id,pem_file_path,vpc_id,instance_type)
                    completed_request_index_list.append(spot_request_id_list.index(spot_instance_request_id))

                if spot_instance_request['Status']['Code'].find('price-too-low') != -1:
                    logger.error("spot instance request %s has not been fullfilled,reason %s",spot_instance_request_id,spot_instance_request['Status']['Message'])
                    completed_request_index_list.append(spot_request_id_list.index(spot_instance_request_id))
            
            completed_request_index_list.sort(reverse=True)
            for completed_request_index in completed_request_index_list:
                del spot_request_id_list[completed_request_index]
        except Exception,e:
            print e

        time.sleep(2)

def create_instance(d,only_check=False):
    
    global instance_db

    params = d['input']
    name = params['name']
    number = get_int_value(params,'number',1)
    instance_type = get_value(params,'instance_type','t2.micro')
    if not create_vpc(d):
        logger.error("create instance %s type %s number %d fail",name,instance_type,number)
        return [],None

    try:
        keyname,pem_file_path = get_key_pair(d)
    except Exception,e:
        logger.error("%s",e)
        logger.error("create keypair %s fail",d['keypair']['key'])
        return [],None

    tags = get_common_tags(params)
    image_id = get_value(params,'image_id')
    if image_id is None:
        image_id = get_default_ami()
    if image_id is None:
        logger.error("cannt find image_id value")
        return [],None
    
    if keyname is None:
        keyname = get_value(params,'keyname')
        pem_file_path = keyname + ".pem"

    subnet_id = get_value(params,'subnet_id')
    if subnet_id is None:
        logger.error("cannt find subnet_id value")
        return [],None
    
    vpc_id = get_vpc_id(subnet_id)
    if vpc_id is None:
        return [],None

    attach_volumes = get_attach_volumes(params)
    security_group_ids = get_value(params,'security_group_ids')
    device_maps = get_volumes(d)
    place_group = get_place_group(params)
    if not only_check:
        if params.has_key('spot'):
            spot_info = params['spot']
            wait_until_complete = spot_info['wait_until_complete']
            if spot_info.has_key('price'):
                price = spot_info['price']
            else:
                price = get_instace_type_price(instance_type) 
            try:
                args = {
                    'SpotPrice':str(price),
                    'InstanceCount':number,
                    'LaunchSpecification':{
                        'ImageId':image_id,
                        'KeyName': keyname,
                        'SecurityGroupIds' : security_group_ids,
                        'SubnetId':subnet_id,
                        'InstanceType':instance_type
                    }
                   
                }
                if device_maps is not None:
                    args['LaunchSpecification'].update(device_maps)
                if place_group is not None:
                    args['LaunchSpecification'].update(place_group)

                if spot_info.has_key('duration'):
                    duration = int(spot_info['duration'])
                    args.update({'BlockDurationMinutes':duration*60})

                instance_list = client_ec2.request_spot_instances(**args)['SpotInstanceRequests']
            except Exception,e:
                logger.error('%s',e)
                logger.error("create spot instance %s type %s number %d price %s fail",name,instance_type,number,price)
                return [],None

            logger.info("create spot instance %s type %s number %d price %s success",name,instance_type,number,price)
            spot_request_id_list = []
            for spot_instance_request in instance_list:
                spot_instance_request_id = spot_instance_request['SpotInstanceRequestId']
                spot_request_id_list.append(spot_instance_request_id)

            one_spot_request = spot_request_id_list[0]
            if wait_until_complete:
                logger.info("start to wait for spot instance request to compelete")
                t = threading.Thread(target=monitor_spot_requests,args=(spot_request_id_list,tags,pem_file_path,vpc_id))
                t.daemon = True
                t.start()
                t.join(1800)
            attach_spot_instance(one_spot_request,attach_volumes)
        else:
            try:
                args = {
                    'ImageId':image_id,
                    'MinCount':number,
                    'MaxCount': number,
                    'KeyName': keyname,
                    'SecurityGroupIds' : security_group_ids,
                    'SubnetId':subnet_id,
                    'InstanceType':instance_type
                }
                if device_maps is not None:
                    args.update(device_maps)
                if place_group is not None:
                    args.update(place_group)

                instance_list = ec2.create_instances(**args)
            except Exception,e:
                logger.error('%s',e)
                logger.error("create instance %s type %s number %d fail",name,instance_type,number)
                return [],None

            tag_name = ""
            if len(tags) > 0:
                tag_name = tags[0]['Value']
                instance_ids = []
                for instance in instance_list:
                    instance_id = instance.id
                    instance_ids.append(instance_id)
                create_instance_tags(instance_ids,tags)
    
            for instance in instance_list:
                logger.info("launch instance id is %s",instance.id)
                instance_db.save_instance_info(instance.id,tag_name,image_id,keyname,security_group_ids[0],subnet_id,pem_file_path,vpc_id,instance_type)
            logger.info("create instance %s type %s number %d success",name,instance_type,number)
            wait_for_attach_instance(instance.id,attach_volumes)
 
    return instance_list,pem_file_path

def attach_spot_instance(spot_request,volumes):

    if not volumes:
        return
    req = client_ec2.describe_spot_instance_requests(SpotInstanceRequestIds = [spot_request])
    spot_instance_requests = req['SpotInstanceRequests']
    spot_instance_request = spot_instance_requests[0]
    spot_instance_request_id = spot_instance_request['SpotInstanceRequestId']
    if spot_instance_request['State'] == 'active':
        instance_id = spot_instance_request['InstanceId']
        wait_for_attach_instance(instance_id,volumes)
    else:
        logger.error("spot request is not active,attach volumes fail")
 

def wait_for_attach_instance(instance_id,volumes):
    if not volumes:
        return
    while True:
        instance = ec2.Instance(instance_id)
        state_name = instance.state['Name']
        if state_name == 'running':
            c = 'f'
            n = ord(c)
            for volume_id in volumes:
                s = chr(n)
                dev = "/dev/xvd" + s
                client_ec2.attach_volume(VolumeId=volume_id,InstanceId=instance_id,Device = dev)
                n += 1
            break
        time.sleep(1)

def ssh_connect_instance(instance,pem_file_path):

    def waitfor_instance_run(instance_id):
        while True:
            instance = ec2.Instance(instance_id)
            state_name = instance.state['Name']
            if state_name == 'running':
                logger.info('instance %s is state %s ,start to connect',instance.id,state_name)
                time.sleep(8)
                break
            logger.info('instance %s state %s',instance.id,state_name)
            time.sleep(1)

    if instance is None:
        logger.error("can not connect none instance")
        return

    instance_id = instance.id
    t = threading.Thread(target=waitfor_instance_run,args=(instance_id,))
    t.daemon = True
    t.start()
    t.join(60)

    instance = ec2.Instance(instance_id)
    public_ip = instance.public_ip_address 
    cmd = "ssh -i %s ubuntu@%s" % (pem_file_path,public_ip)
    logger.info("%s",cmd)
    os.system(cmd)

def create_all_instance_from_config(yaml_config_path):
    create_all_from_config(yaml_config_path,'instance',create_instance)
    
def create_default_instance_from_config(yaml_config_path):
    try:
        nodes = load_yaml_config(yaml_config_path)
    except Exception,e:
        logger.error("%s",e)
        return None,None

    d = nodes[0]['instance']
    instances,pem_file_path = create_instance(d)
    if 0 == len(instances):
        return None,None

    return instances[0],pem_file_path 

def lanuch_default_instance():
    
    data_dir = os.path.abspath(os.path.split(__file__)[0])
    region = utils.get_region()
    instance_config_file = './data/default_instance_config.yaml'
    if region is not None:
        instance_config_file = './data/default_instance_region_' + region + "_config.yaml"
    default_config_path = os.path.join(data_dir,instance_config_file)
    return create_default_instance_from_config(default_config_path)

def check_keypair_exists(keyname,key_path_file):

    if not os.path.exists(key_path_file):
        return False
    try:
        key_pair = ec2.KeyPair(keyname)
        key_pair.load()
        return True

    except Exception,e:
        logger.warn("%s",e)
        return False

def launch_one_instance(instance_type,volume_size):

    global instance_db

    result = instance_db.load_default_config()
    if result is None:
        return lanuch_default_instance()
    else:
        subnet_id,keyname,security_group_id,image_id,key_path_file = result
        if not check_keypair_exists(keyname,key_path_file):
            logger.warn("key file %s is not exists,will create new key",key_path_file)
            key_path = os.path.dirname(key_path_file)
            try:
                key_path_file = create_key_pair(keyname,True,path=key_path)
            except Exception,e:
                logger.error("%s",e)
                return None,None

        try:
            args = {
                'ImageId':image_id,
                'MinCount':1,
                'MaxCount': 1,
                'KeyName': keyname,
                'SecurityGroupIds' : [security_group_id],
                'SubnetId':subnet_id,
                'InstanceType':instance_type,
                'BlockDeviceMappings':[
                    {
                        'Ebs':{
                            'VolumeSize':volume_size
                        },
                        'DeviceName':'/dev/sda1' 
                    }
                ]
            }
            instance_list = ec2.create_instances(**args)
            logger.info("create instance type %s success",instance_type)
            return instance_list[0],key_path_file
        except Exception,e:
            logger.warn("%s",e)
            return lanuch_default_instance()

def find_instance_by_name(name,output):

    if output not in ['n','c']:
        logger.error("output option is n which output by line ,c which output by comma")
        return

    global instance_db
    instances = instance_db.get_instance_by_tag(name)
    for instance_info in instances:
        if output == 'n':
            print instance_info[0]
        elif output == 'c':
            import sys
            if instance_info == instances[-1]:
                sys.stdout.write(instance_info[0])
                #print instance_info[0],
            else:
                sys.stdout.write(instance_info[0])
                sys.stdout.write(",")
                #print instance_info[0],',',

def deal_one_instance(str_instance_id,action,**kwargs):

    global instance_db

    if action == "find":
        name = kwargs['tag']
        output = kwargs['output']
        find_instance_by_name(name,output)
        return

    instance_ids = str_instance_id.split(',')
    for instance_id in instance_ids:
        instance = ec2.Instance(instance_id)
        try:
            if action == "stop":
                instance.stop()
            elif action == "reboot":
                instance.reboot()
            elif action == "term":
                instance_db.delete_instance_info(instance_id)
                instance.terminate()
            elif action == "start":
                instance.start()
            else:
                raise ValueError("invalid action %s,possible action option is stop,reboot,term,start" % (action))
        except Exception,e:
            logger.error("%s",e)
            logger.error("%s instance %s fail",action,instance_id)
            continue
        logger.info("%s instance %s success",action,instance_id)

def create_instance_tags(instance_ids,tags):

    for i in range(50):
        try:
            client_ec2.create_tags(Resources=instance_ids,Tags=tags)
            break
        except Exception,e:
            logger.error("create instances tag error %s",e)
            time.sleep(1)

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, dest="config_file_path")
    parser.add_argument("-launch-one-instance", action='store_true', dest="is_launch_one_instance",default=False)
    parser.add_argument("-type", type=str, dest="instance_type",default=config.DEFAULT_INSTANCE_TYPE)
    parser.add_argument("-volume", type=int, dest="instance_volume_size",default=config.DEFAULT_INSTANCE_VOLUME_SIZE)
    parser.add_argument("-connect-after-launch", action='store_true', dest="is_connect_after_lauch",default=False)
    parser.add_argument("-i", "--id", type=str, dest="instance_id")
    parser.add_argument("-a", "--action", type=str, dest="action")
    parser.add_argument("-tag", type=str, dest="tag")
    parser.add_argument("-o", type=str, dest="output",default="n")
    enable_debug_log(True)
    args = parser.parse_args()
    if args.is_launch_one_instance:
        instance,key_path = launch_one_instance(args.instance_type,args.instance_volume_size)
        if args.is_connect_after_lauch:
            ssh_connect_instance(instance,key_path)
    elif args.action is not None:
        kwargs = {
            'tag':args.tag,
            'output':args.output
        }
        deal_one_instance(args.instance_id,args.action,**kwargs)
    else:
        yaml_config_path = args.config_file_path
        create_all_instance_from_config(yaml_config_path)

if __name__ == "__main__":
    main()
    
