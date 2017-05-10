#!/usr/bin/python
import subprocess, json, base64, string, random, sys

input_json = json.load(sys.stdin)

required = ["uaa_uri",
            "uaa_client_secret",
            "client_payloads"]

missing = filter(lambda key: key not in input_json, required)
if missing:
    raise Exception("missing input argument(s) {}"
                    .format(",".join(missing)))
uaa_uri = input_json["uaa_uri"]
uaa_secret = input_json["uaa_client_secret"]
uaa_clients_endpoint = "{}/oauth/clients".format(uaa_uri)
client_payloads = input_json["client_payloads"]
# base64_encode of client id and client secret
base64_encode = base64.b64encode("admin:{}".format(uaa_secret))

curl_uaa_uri = "{}/oauth/token?grant_type=client_credentials".format(uaa_uri)

authorization_field = "Authorization: Basic {}".format(base64_encode)

get_token_args = ["curl", "-sS", "-X", "GET", curl_uaa_uri,
                  "-H", authorization_field,
                  "-H", "Content-Type: application/x-www-form-urlencoded",
                  "-H", "Accept: application/json"]

response_json = subprocess.check_output(get_token_args)


try:
    response_dict = json.loads(response_json)
except:
    raise Exception("non JSON response from server:\n {}".
                    format(response_json))


if not "access_token" in response_dict:
    json.dump(response_dict, sys.stderr)
    raise Exception("no access_token in response")

token = response_dict["access_token"]


for client_payload in client_payloads :
  client_id = client_payload["client_id"]
  payload = json.dumps(client_payload)
  authorization = "Authorization:bearer {}".format(token)

  create_uaa_client_args = ["curl", "-sS", "-X", "POST",
                            uaa_clients_endpoint, "-d", payload, "-H",
                            authorization, "-H", "Content-Type: application/json",
                            "-H", "Accept: application/json"]

  resp_json = subprocess.check_output(create_uaa_client_args)
  try:
      resp_dict = json.loads(resp_json)
  except:
      raise Exception("non JSON response from server:\n {}".
                    format(resp_json))

  if resp_dict.get("error_description")==\
     "Client already exists: {}".format(client_id):
    delete_uaa_client_args = ["curl", "-sS", "-X",
                              "DELETE", uaa_clients_endpoint+"/"+client_id, "-H",
                              authorization, "-H", "Content-Type: application/json"]
    subprocess.check_output(delete_uaa_client_args)
    subprocess.check_output(create_uaa_client_args)



print ("{}")
