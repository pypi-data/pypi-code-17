class GameData:

    def __init__(self, leagues, tiers, divisions, ladders, teams):
        self._leagues = leagues
        self._tiers = tiers
        self._divisions = divisions
        self._ladders = ladders
        self._teams = teams

    def leagues(self):
        return self._leagues

    def tiers(self):
        return self._tiers

    def divisions(self):
        return self._divisions

    def ladders(self):
        return self._ladders

    def teams(self):
        return self._teams
