import time

from .download import get_current_season_data
from .download import get_game_data
from .download import get_ladder_data
from .download import get_league_data
from .token import get_access_token


class Sc2GameDataClient:
    def __init__(self, client_id: str, client_secret: str):
        self._client_id = client_id
        self._client_secret = client_secret

        self._access_tokens = {}
        self._access_token_expiries = {}

    def _refresh_token_if_expired(self, region: str):
        if region not in self._access_token_expiries or self._access_token_expiries[region] < time.time():
            access_token, expiry = get_access_token(self._client_id, self._client_secret, region)
            self._access_tokens[region] = access_token
            self._access_token_expiries = expiry

    def get_current_season_data(self, region: str) -> dict:
        self._refresh_token_if_expired(region)
        return get_current_season_data(self._access_tokens[region], region)

    def get_game_data(self, workers: int, region: str) -> dict:
        self._refresh_token_if_expired(region)
        return get_game_data(self._access_tokens[region], workers, region)

    def get_ladder_data(self, ladder_id: int, region: str) -> dict:
        self._refresh_token_if_expired(region)
        return get_ladder_data(self._access_tokens[region], ladder_id, region)

    def get_league_data(self, season: int, league_id: int, region: str) -> dict:
        self._refresh_token_if_expired(region)
        return get_league_data(self._access_tokens[region], season, league_id, region)