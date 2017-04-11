import time
import urllib.error
import urllib.request
import json

from .download import get_current_season_data
from .download import get_game_data
from .download import get_ladder_data
from .download import get_league_data

OAUTH_AUTHENTICATION_TEMPLATE = "https://{}.battle.net/oauth/token?grant_type=client_credentials&client_id={}&client_secret={}"


class Sc2GameDataClient:
    def __init__(self, client_id: str, client_secret: str):
        self._client_id = client_id
        self._client_secret = client_secret

        self._access_tokens = {}
        self._access_token_expiries = {}

    def _refresh_token_if_expired(self, retries_so_far: int, region: str):
        if region not in self._access_token_expiries or self._access_token_expiries[region] < time.time():
            try:
                path = OAUTH_AUTHENTICATION_TEMPLATE.format(region, self._client_id, self._client_secret)

                with urllib.request.urlopen(path) as response:
                    response_str = response.read().decode('utf8')
                response_data = json.loads(response_str)

                self._access_token_expiries[region] = time.time() + response_data["expires_in"]
                self._access_tokens[region] = response_data["access_token"]
            except urllib.error.HTTPError as e:
                time.sleep(2)
                if retries_so_far < 10:
                    self._refresh_token_if_expired(retries_so_far + 1, region)
                else:
                    raise e

    def get_current_season_data(self, region: str) -> dict:
        self._refresh_token_if_expired(0, region)
        return get_current_season_data(self._access_tokens[region], region)

    def get_game_data(self, workers: int, region: str) -> dict:
        self._refresh_token_if_expired(0, region)
        return get_game_data(self._access_tokens[region], workers, region)

    def get_ladder_data(self, ladder_id: int, region: str) -> dict:
        self._refresh_token_if_expired(0, region)
        return get_ladder_data(self._access_tokens[region], ladder_id, region)

    def get_league_data(self, season: int, league_id: int, region: str) -> dict:
        self._refresh_token_if_expired(0, region)
        return get_league_data(self._access_tokens[region], season, league_id, region)