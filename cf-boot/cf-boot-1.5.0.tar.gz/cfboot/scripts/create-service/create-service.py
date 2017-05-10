#!/usr/bin/python
from __future__ import print_function
import subprocess, os, json, random, sys
import time, re

input_json = json.load(sys.stdin)

required_input = ["instance_name",
            	  "service",
            	  "plan",
            	  "cf_home"]

missing = filter(lambda key: key not in input_json, required_input)
if missing:
    raise Exception("missing input argument(s) {}"
                    .format(",".join(missing)))

#optional payload argument
payload_args = []
if "payload" in input_json:
		payload_args = ["-c", json.dumps(input_json["payload"])]

args = ["cf", "create-service",
        input_json["service"], input_json["plan"],
        input_json["instance_name"]] + payload_args

os.environ["CF_HOME"] = input_json["cf_home"]
child_env = os.environ.copy()

p = subprocess.Popen(args, env = child_env, stdout=sys.stderr)
p.wait()
if p.returncode != 0:
    raise Exception("create {} service failed with args: {}"
                    .format(input_json["service"],args))

guid = subprocess.check_output(
		["cf", "service", input_json["instance_name"], "--guid"],
		env = child_env).rstrip()

DELAY_SECS = 10
while True:
    out = subprocess.check_output(
            ["cf", "curl", "v2/service_instances/{}".format(guid)],
            env = child_env)
    last_operation = json.loads(out)["entity"]["last_operation"]
    (op_type, op_status) = last_operation["type"], last_operation["state"]
    if op_type=="create" and op_status=="progress":
        print ("provisioning in progress: {} {}. sleeping for {} secs..."
               .format(op_type, op_status, DELAY_SECS),
               file = sys.stderr)
        time.sleep(DELAY_SECS)
    else:
        break

print (json.dumps({"SERVICE_GUID" : guid}))
