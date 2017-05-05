import network as Network
import compute as Compute
import compilescripts as Compiler
import json

networking_details = None
compute_details = None

def getSegment(filepath, segment, config, stage):
    networking_details = Network.compile(filepath, config, stage)
    if segment == "network":
        return networking_details
    elif segment == "compute":
        compute_details = Compute.compile(filepath, config, stage, networking_details)
        return compute_details
    elif segment == "all":
        compute_details = Compute.compile(filepath, config, stage, networking_details)
        config["stage"] = stage
        base = Compiler.loadfile(filepath, "./Infrastructure/base.json", config, {})
        all_segments = {}
        regions = config.get("regions")
        for region in regions:
            config["region"] = region
            all_segments[region] = {
                "Resources": {},
                "Mappings": {}
            }
            for key in networking_details[region]:
                network = networking_details[region][key]
                network_resources = network["resources"]
                # network_resources = json.loads(network_resources)
                for resource_key in network_resources:
                    all_segments[region]["Resources"][resource_key] = network_resources[resource_key]
            for key in compute_details[region]:
                network = compute_details[region][key]
                for resource_key in network:
                    all_segments[region]["Resources"][resource_key] = network[resource_key]
            for key in base:
                all_segments[region][key] = base[key]
            mappings = open('./Infrastructure/mappings.json', "r").read()
            mappings = json.loads(mappings)
            for key in mappings:
                all_segments[region]["Mappings"][key] = mappings[key]
        return all_segments
    return None








