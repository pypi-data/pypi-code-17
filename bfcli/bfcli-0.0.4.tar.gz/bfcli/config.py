import json
import os

import jsonschema
import yaml

conf = {}
config_file_path = os.path.expanduser('~/.bfcli.conf')

config_schema = """
type: object

required:
  - host
  - uid
  - username

properties:
  host:
    type: string
    pattern: "^http(s)?://"
  username:
    type: string
  uid:
    type: string
  cookies:
    type: object
"""

# This is set in the API library
user = None

try:
  with open(config_file_path, 'r') as f:
    # This returns None if the file is empty
    conf = yaml.load(f)
except:
  pass
finally:
  if not conf:
    conf = {}


def validate_config(config=conf):
  return jsonschema.validate(config, yaml.load(config_schema))


def save_config(**kwargs):
  config = yaml.load(json.dumps(kwargs))

  with open(config_file_path, 'w') as f:
    yaml.dump(config, f, default_flow_style=False)
