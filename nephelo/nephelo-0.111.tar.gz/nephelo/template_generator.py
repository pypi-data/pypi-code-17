import json
import os
import sys
import segments as Segments


def saveTemplates(config, stage):
    config["stage"] = stage
    resources = Segments.getSegment("", "all", config, stage)
    regions = config.get("regions")
    if not os.path.exists("./dist"):
        os.makedirs("./dist")
    if not os.path.exists("./dist/" + stage + "/"):
        os.makedirs("./dist/" + stage + "/")
    for region in regions:
        filepath = "./dist/" + stage + "/" + region + ".json"
        region_json = resources[region]
        with open(filepath, "w") as text_file:
            text_file.write(json.dumps(region_json))
    return None