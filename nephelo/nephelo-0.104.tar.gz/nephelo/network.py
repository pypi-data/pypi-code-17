import compilescripts as Compiler
import os
import boto3
from netaddr import IPNetwork
import json
import math



def getsubnetsforregion(regionname):
    print regionname


def compile(libpath, config, stage):
    regions = config.get("regions")
    pathtocore = "./Infrastructure/Resources/Networking/"

    # need to work out the cidr blocks

    # how many networks are there? the top level CIDR block needs to be split across

    networks = []
    for level in os.walk(pathtocore):
        networks = level[1]
        break
    individual_networks = {}
    for network in networks:
        for region in regions:
            networkname = Compiler.deCamel(network)
            individual_networks[network + ":" + region] = {
                "vpc_name": "vpc" + stage + region.replace("-", "") + networkname
            }
    number_of_cidr_blocks = len(individual_networks.keys())
    subnets = splitCidrBlock(config.get("cidr_block"), number_of_cidr_blocks)
    print subnets
    for key in individual_networks:
        print subnets
        individual_networks[key]["cidr_block"] = subnets.pop(0)
    network_json = {}
    for region in regions:

        region_network_data = {}
        for network in networks:
            # create the vpc
            networkname = Compiler.deCamel(network)
            network_record = individual_networks[network + ":" + region]
            vpc = generateVpc(region, stage, network_record["vpc_name"], network_record["cidr_block"])
            # create the subnets
            subnets = generatesubnets(region, networkname, network_record["vpc_name"], stage, network_record["cidr_block"])
            subnet_ids = subnets.keys()
            subnet_ids = map(lambda x: "{\"Ref\":\"" + x + "\"}", subnet_ids)
            # compile the path
            config["region"] = region
            resources = Compiler.compilePath(libpath, pathtocore + network + "/", config, stage, {
                "vpc-id": network_record["vpc_name"],
                "subnet-ids": subnet_ids,
                "raw-subnet-ids": subnets.keys()
            })
            networkresources = {}
            for vpckey in vpc:
                networkresources[vpckey] = vpc[vpckey]
            for subnetkey in subnets:
                networkresources[subnetkey] = subnets[subnetkey]
            for resourcekey in resources:
                networkresources[resourcekey] = resources[resourcekey]
            region_network_data[network] = {
                "resources": networkresources,
                "cidr_block": network_record["cidr_block"],
                "subnet_ids": subnet_ids,
                "vpc_id": network_record["vpc_name"],
                "raw_subnet_ids": subnets.keys()
            }
        network_json[region] = region_network_data

    return network_json


def subnetids():
    return "\"\""


def generatesubnets(region, networkname, vpcid, stage, network_block):
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    subnet_template = templates_dir + "/subnet.json"
    zones = getZonesForRegion(region)
    subnet_blocks = splitCidrBlock(network_block, len(zones))
    subnets = {

    }
    for zone in zones:
        subnet_string = open(subnet_template).read()
        subnet_name = vpcid.replace("vpc", "subnet" + zone)
        cidr_block = subnet_blocks.pop(0)
        vpc_reference = "{\"Ref\":\"" + vpcid + "\"}"
        name = vpcid.replace("vpc", "subnet" + zone)
        subnet_string = subnet_string.replace("{SUBNETNAME}", subnet_name)
        subnet_string = subnet_string.replace("{NAME}", subnet_name)
        subnet_string = subnet_string.replace("{STAGE}", stage)
        subnet_string = subnet_string.replace("{CIDR_BLOCK}", cidr_block)
        subnet_string = subnet_string.replace("{AVAILABILITY_ZONE}", zone)
        subnet_string = subnet_string.replace("\"{VPC_REFERENCE}\"", vpc_reference)
        subnets[subnet_name.replace("-", "")] = json.loads(subnet_string)
    return subnets


def generateVpc(region, stage, vpc_name, cidr_block):
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    vpc_template = templates_dir + "/vpc.json"
    vpcstring = open(vpc_template).read()
    vpcstring = vpcstring.replace("{VPC_NAME}", vpc_name.replace("-", ""))
    vpcstring = vpcstring.replace("{NAME}", vpc_name)
    vpcstring = vpcstring.replace("{CIDR_BLOCK}", cidr_block)
    vpcstring = vpcstring.replace("{STAGE}", stage)
    return json.loads(vpcstring)


def getZonesForRegion(region):
    availZones = []
    ec2 = boto3.client('ec2', region_name=region)
    for zone in ec2.describe_availability_zones()['AvailabilityZones']:
        if zone['State'] == 'available':
            availZones.append(zone['ZoneName'])
    return availZones


def splitCidrBlock(cidr_block, number_of_cidr_blocks):
    net = IPNetwork(cidr_block)
    current_cidr_exponent = int(cidr_block.split("/")[-1])
    exponent_difference = math.log(number_of_cidr_blocks, 2)
    exponent_difference = math.ceil(exponent_difference)
    exponent_difference = int(exponent_difference)
    subnets = net.subnet(current_cidr_exponent + exponent_difference)
    subnets = list(subnets)
    if len(subnets) == 0:
        subnets.append(cidr_block)
    subnets = map(lambda x: str(x), subnets)
    print subnets
    return subnets