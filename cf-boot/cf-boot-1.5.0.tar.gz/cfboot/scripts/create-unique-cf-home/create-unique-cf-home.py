#!/usr/bin/python
import subprocess, os, json, random, sys
import hashlib

input_json = json.load(sys.stdin)

required = ["CF_TARGET",
            "CF_USER",
            "CF_PASSWORD",]

missing = filter(lambda key: key not in input_json, required)
if missing:
    raise Exception("missing input argument(s) {}"
                    .format(",".join(missing)))



if not set(("CF_ORG", "CF_SPACE")).difference(input_json.keys()):
    org = input_json["CF_ORG"]
    space = input_json["CF_SPACE"]
elif "CF_ORG_SPACE" in input_json:
    (org, space) = input_json["CF_ORG_SPACE"].split("/")
else:
    raise Exception("{CF_ORG,CF_SPACE} or CF_ORG_SPACE inputs required")


args = ["cf", "login",
        "-a", input_json["CF_TARGET"],
        "-u", input_json["CF_USER"],
        "-p", input_json["CF_PASSWORD"],
        "-o", org,
        "-s", space]

def md5_hash ( string ):
    md5 = hashlib.md5()
    md5.update(string)
    return md5.hexdigest()

cf_home_md5 = md5_hash(" ".join(args))
cf_home_unique = os.path.join("/tmp", "cf-homes", cf_home_md5)

if not os.path.exists(cf_home_unique):
    os.makedirs(cf_home_unique)

os.environ["CF_HOME"] = cf_home_unique
child_env = os.environ.copy()
p = subprocess.Popen(args, env = child_env, stdout=sys.stderr)
p.wait()
if p.returncode != 0:
    raise Exception("error running cf login")

json.dump({"CF_HOME" : cf_home_unique}, sys.stdout)
