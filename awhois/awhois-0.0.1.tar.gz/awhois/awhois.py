#!/usr/bin/env python3

import boto3
import sys
import ipaddress

def main(ipaddr):
    instance = search_network(ipaddr)
    instance = search_ec2(ipaddr)

    if instance:
        print('Tags: ')
        for tag in instance.tags:
            print(' ', tag['Key'],': ', tag['Value'])

def search_ec2(ipaddr):
    global conf

    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
        Filters=[{'Name': 'private-ip-address', 'Values': [ipaddr]}]
    )
    for instance in instances:
        print('EC2 Information:')
        print('  Id: ', instance.id)
        print('  Type:', instance.instance_type)
        print('  State :', instance.state['Name'])
        print('  Private IP: ', instance.private_ip_address)
        print('  Public IP: ', instance.public_ip_address)
        print('  Launch Time: ', instance.launch_time)
        return instance
    return False

def search_network(ipaddr):
    ec2 = boto3.resource('ec2')
    instances = ec2.network_interfaces.filter(
        Filters=[{'Name': 'private-ip-address', 'Values': [ipaddr]}]
    )
    for instance in instances:
        print('Instance :')
        print('  Id: ', instance.id)
        print('  Description: ', instance.description)
        print('  Status: ', instance.status)
        print('  Private DNS name: ', instance.private_dns_name)
        print('  Private IP Address: ', instance.private_ip_address)
        print('  Availability Zone: ', instance.availability_zone)
        print('  Subnet: ', instance.subnet.id)
        print('  VPC: ', instance.vpc_id)
        print('  Owner ID: ', instance.owner_id)
    return False

# Check for new version
#if conf['last-version'] is None or conf['last-version']:


# Testing argument
if len(sys.argv) == 1:
    print()
    print("No IP found!")
    print(" Usage: {} <ipaddr>".format(sys.argv[0]))
    print()
    print(" * To configure your AWS credentials, please run: aws configure")
    print()
    sys.exit(1)

ipaddr = sys.argv[1]

# Test IP address format
try:
    ipaddress.ip_address(ipaddr)
except Exception as e:
    print("'{}' is not a valid IPv4 or IPv6 address".format(ipaddr))
    sys.exit(1)
try:
    main(ipaddr)
except Exception as e:
    print()
    print(e)
    print()
    print("To set your AWS credentials properly, please run: aws configure")
    print()
