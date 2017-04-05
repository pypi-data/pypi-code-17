def luacode(insert: str=None) -> str:

    if insert is None or len(insert) == 0:
        insert = ''
    else:
        insert = f'\n{insert}'

    return f'''
playerShip = getPlayerShip(-1){insert}
energyLevel = playerShip:getEnergyLevel()
energyLevelMax = playerShip:getEnergyLevelMax()
alertLevel = playerShip:getAlertLevel()
shieldsActive = playerShip:getShieldsActive()
hull = playerShip:getHull()
hullMax = playerShip:getHullMax()

return {{
    energyLevel=energyLevel,
    energyLevelMax=energyLevelMax,
    hull = hull,
    hullMax = hullMax,
    shieldsActive=shieldsActive,
    alertLevel=alertLevel,
}}
'''

def statement_for(action: str, value) -> str:
    if action == 'hull':
        return f'playerShip:setHull({value})\n'

    if action == 'energy':
        return f'playerShip:setEnergyLevel({value})\n'

    valid_actions = ['hull', 'energy']
    raise ValueError(f'Please supply action, being one of {valid_actions}')
