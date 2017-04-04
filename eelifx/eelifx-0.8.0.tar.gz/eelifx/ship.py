class Ship():
    def __init__(self):
        self._alert_level = 'normal'
        self._shields_active = False
        self._shields_transitioned = False
        self._energy = 1.0
        self._hull = 1.0

    def update(self, lua_response):
        self._alert_level = lua_response['alertLevel']
        self._shields_transitioned = (self._shields_active != lua_response['shieldsActive'])
        self._shields_active = lua_response['shieldsActive']
        self._energy = lua_response['energyLevel'] / lua_response['energyLevelMax']
        self._hull = lua_response['hull'] / lua_response['hullMax']

    @property
    def alert_level(self):
        return self._alert_level

    @property
    def shields_active(self):
        return self._shields_active

    @property
    def shields_transitioned(self):
        return self._shields_transitioned

    @property
    def energy(self):
        return self._energy

    @property
    def hull(self):
        return self._hull

    def to_dict(self):
        data = {}
        data['alert_level'] = self.alert_level
        data['shields_active'] = self.shields_active
        data['shields_transitioned'] = self.shields_transitioned
        data['energy'] = self.energy
        data['hull'] = self.hull

        return data

    def __repr__(self):
        res = ''
        for k, v in self.to_dict().items():
            res += " {key}={value}".format(key=k, value=v)

        return '<Ship{res}>'.format(res=res)
