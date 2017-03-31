'''
AWS Information Script - Dan P
Search for amazon instance by ID, Name tag or IP ip_address
The boto python library will look for credentials matching each profile in ~/.aws/credentials file
http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
'''
import sys
import re
import os
import ConfigParser
import pickle
from threading import Thread
import argparse
import pkg_resources
import boto.ec2


profile = None
regions = None
cache_file = None

all_instances = []

def print_line(key, value):
    print "{0}:\t{1}".format(key, value)


def search_for_instance_using_known_field(search_field, search_string):
    all_instances_from_cache = get_all_servers_from_cache_file()

    if search_field == "name":
        found_instances = [instance for instance in all_instances_from_cache if search_string.lower() in instance['name'].lower()]
    elif search_field == "id":
        found_instances = [instance for instance in all_instances_from_cache if search_string in instance['id']]
    else:
        found_instances = [instance for instance in all_instances_from_cache if instance[search_field] == search_string]

    if not found_instances:
        print "Not Found. Consider running a refresh if you think this is a mistake"
        sys.exit(0)
    elif len(found_instances) > 1:
        print_multiple_warning(found_instances)
        sys.exit()
    else:
        return found_instances[0]


def print_multiple_warning(instances):
    print "More than one instance found, use a different field to be more precise"
    for instance in instances:
        print_instance_info(instance)


def print_instance_info(instance):
    print ''
    print_line('Name', instance['name'])
    print_line('Acc', instance['acc'])
    print_line('AZ', instance['az'])
    print_line('ID', instance['id'])
    print_line('IP', instance['ip'])
    print_line('PriIP', instance['priip'])
    print_line('Type', instance['type'])
    print_line('State', instance['state'])
    print_line('Key', instance['key'])
    print_line('Launch', instance['launch_time'])
    print_line('DNS', instance['dns'])
    print_line('ssh', generate_ssh_command_string(instance))
    print ''


def generate_ssh_command_string(instance):
    return "ssh -o StrictHostKeyChecking=no ec2-user@{} -i {}/.ssh/{}.pem".format(choose_ip_to_use(instance), os.path.expanduser("~"), instance['key'])


def choose_ip_to_use(instance):
    if instance['usePrivateIp']:
        return instance['priip']
    elif instance['priip'] and not instance['ip']:
        return instance['priip']
    return instance['ip']


def open_ssh_session(instance):
    ssh_key_path = "{}/.ssh/{}.pem".format(os.path.expanduser("~"), instance['key'])
    if instance['state'] == 'running':
        if os.path.isfile(ssh_key_path):
            try:
                raw_input('Press enter to continue...\n')
                os.system(generate_ssh_command_string(instance))
            except KeyboardInterrupt:
                print "Cancelled"
        else:
            print "ERROR: ssh key {} not found".format(ssh_key_path)


def print_usage():
    print "usage awsi [refresh|list|i-12345|54.32.10.01|Live Web Server 01]"


def load_config():
    global profiles
    global regions
    global cache_file

    config_file = '~/.awsi/config.cfg'

    if not os.path.exists(os.path.expanduser(config_file)):
        print "ERROR: missing config file " + config_file
        sys.exit(1)

    config = ConfigParser.ConfigParser()
    config.read(os.path.expanduser(config_file))
    regions = config.get('main', 'regions').split(',')
    profiles = config.get('main', 'profiles').split(',')
    cache_file = config.get('main', 'cache_file')


def retrieve_servers_from_aws_account(profile):
    global all_instances

    for region in regions:
        print "[re]caching {0} {1}".format(profile, region)
        conn = boto.ec2.connect_to_region(region, profile_name=profile)
        instances = [
            instance
            for reservations in conn.get_all_instances()
            for instance in reservations.instances
        ]
        for instance in instances:
            all_instances.append({
                "id":instance.id,
                "name": instance.tags.get('Name', 'no-name-assigned'),
                "ip":instance.ip_address,
                "priip":instance.private_ip_address,
                "acc":profile,
                "az":instance.placement,
                "type":instance.instance_type,
                "state":instance.state,
                "key":instance.key_name,
                "dns":instance.public_dns_name,
                "launch_time":instance.launch_time,
                "usePrivateIp": False
            })
        conn.close()


def refresh_cache():
    global all_instances
    threads = []
    try:
        for profile in profiles:
            thread = Thread(name="Thread-{}".format(profile), target=retrieve_servers_from_aws_account, args=(profile,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        with open(cache_file, 'w') as files:
            pickle.dump(all_instances, files)

        print "Cache written to {}".format(cache_file)
    except boto.provider.ProfileNotFoundError:
        print "profile '{}' not found in aws config".format(profile)
    except KeyboardInterrupt:
        print "Cancelled"
    except Exception as error:
        print error.message
        sys.exit(1)


def get_all_servers_from_cache_file():
    try:
        with open(cache_file, 'r') as file:
            return pickle.load(file)
    except IOError as error:
        print error
        print "Cache file not found, run awsi refresh to generate it"
        sys.exit(1)


def print_cache():
    sorted_list = sorted(get_all_servers_from_cache_file(), key=lambda k: k['name'])
    for instance in sorted_list:
        print instance['name']


def establish_which_field_to_search_by_from_args(arg_string):
    private_ip_re = re.compile(
        r'(^127\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$)|'
        r'(^10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$)|'
        r'(^172\.1[6-9]{1}[0-9]{0,1}\.[0-9]{1,3}\.[0-9]{1,3}$)|'
        r'(^172\.2[0-9]{1}[0-9]{0,1}\.[0-9]{1,3}\.[0-9]{1,3}$)|'
        r'(^172\.3[0-1]{1}[0-9]{0,1}\.[0-9]{1,3}\.[0-9]{1,3}$)|'
        r'(^192\.168\.[0-9]{1,3}\.[0-9]{1,3})$'
    )
    ip_re = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    id_8_re = re.compile(r'^i-.{8}$')
    id_17_re = re.compile(r'^i-.{17}$')

    if private_ip_re.match(arg_string):
        return "priip"
    elif ip_re.match(arg_string):
        return "ip"
    elif id_8_re.match(arg_string) or id_17_re.match(arg_string):
        return "id"
    else:
        return "name"


def main():

    parser = argparse.ArgumentParser()
    mxgroup = parser.add_mutually_exclusive_group(required=False)
    mxgroup.add_argument('--refresh', help='refresh the cache', action='store_true')
    mxgroup.add_argument('--list', help='list all instances in the cache', action='store_true')
    mxgroup.add_argument('--version', help='print version', action='store_true')
    parser.add_argument('-p', '--privateip', help='use the hosts private ip address', action='store_true')
    parser.add_argument('search_string', nargs='*', help='ip, instance id or string to find in Name tag')

    args = parser.parse_args()

    if not args.list and not args.version and not args.refresh and not args.search_string:
        parser.error('must provide a string to search for')

    search_string = ' '.join(args.search_string)

    load_config()

    if args.refresh:
        refresh_cache()
        sys.exit()
    elif args.list:
        print_cache()
        sys.exit()
    elif args.version:
        print pkg_resources.require("awsi")[0].version
        sys.exit()

    connect_to_instance = None

    search_field = establish_which_field_to_search_by_from_args(search_string)

    connect_to_instance = search_for_instance_using_known_field(search_field, search_string)

    connect_to_instance['usePrivateIp'] = args.privateip

    print_instance_info(connect_to_instance)
    open_ssh_session(connect_to_instance)

if __name__ == '__main__':
    main()
