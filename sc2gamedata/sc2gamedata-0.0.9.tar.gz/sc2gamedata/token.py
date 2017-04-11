import urllib.error
import urllib.request
import json
import time

OAUTH_AUTHENTICATION_TEMPLATE = "https://{}.battle.net/oauth/token?grant_type=client_credentials&client_id={}&client_secret={}"


def get_access_token(client_id: str, client_secret: str, region: str) -> (str, int):
    return _get_access_token_inner(0, client_id, client_secret, region)


def _get_access_token_inner(retries_so_far: int, client_id: str, client_secret: str, region: str) -> (str, int):
    try:
        path = OAUTH_AUTHENTICATION_TEMPLATE.format(region, client_id, client_secret)

        with urllib.request.urlopen(path) as response:
            response_str = response.read().decode('utf8')
        response_data = json.loads(response_str)

        return response_data["access_token"], time.time() + response_data["expires_in"]
    except urllib.error.HTTPError as e:
        time.sleep(2)
        if retries_so_far < 10:
            return _get_access_token_inner(retries_so_far + 1, client_id, client_secret, region)
        else:
            raise e