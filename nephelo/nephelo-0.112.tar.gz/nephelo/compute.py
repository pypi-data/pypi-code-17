import compilescripts as Compiler
import os
import boto3
import json

def compile(libpath, config, stage, network_data):
    regions = config.get("regions")
    pathtocore = "./Infrastructure/Resources/Compute/"
    regional_compute = {}
    networks = []
    for level in os.walk(pathtocore):
        networks = level[1]
        break
    for region in regions:
        regional_compute_data = {}
        for network_name in networks:
            network = network_data[region][network_name]
            config["region"] = region
            resources = Compiler.compilePath(libpath, pathtocore, config, stage, {
                "vpc-id": network["vpc_id"],
                "subnet-ids": network["subnet_ids"],
                "raw-subnet-ids": network["raw_subnet_ids"]
            })
            regional_compute_data[network_name] = resources
        regional_compute[region] = regional_compute_data
    print regional_compute
    return regional_compute
