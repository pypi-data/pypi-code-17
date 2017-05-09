import pandas as pd
import requests
from tempfile import mkdtemp
from joblib import Memory

cachedir = mkdtemp()
memory = Memory(cachedir=cachedir, verbose=0)
STAE_URI = 'https://municipal.systems/v1/municipalities/'

def to_dataframe(func):
    def wrapper(municipalityId):
        return pd.DataFrame(func(municipalityId))
    return wrapper

@memory.cache
@to_dataframe
def fetch_trips(municipalityId):
    '''Retrieve trips for a given municipality.

    Parameters
    ----------
    municipalityId : string
        Stae-specific identifier.

    Returns
    -------
    r : results
        Results are wrapped in pandas dataframe.

    Notes
    -----
    Results are cached locally.

    References
    ----------
    .. [1] https://docs.municipal.systems/reference
    '''
    if type(municipalityId) is not str:
        raise ValueError('Municipality IDs are strings.')  # jersey city is "jers-nj"

    try:
        identifier = STAE_URI + municipalityId + '/trips'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"

@memory.cache
@to_dataframe
def fetch_issues(municipalityId):
    try:
        identifier = STAE_URI + municipalityId + '/issues'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"

@memory.cache
@to_dataframe
def fetch_building_permits(municipalityId):
    try:
        identifier = STAE_URI + municipalityId + '/building_permits'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"

@memory.cache
@to_dataframe
def fetch_businesses(municipalityId):
    try:
    	identifier = STAE_URI + municipalityId + '/businesses'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"

@memory.cache
@to_dataframe
def fetch_bike_lanes(municipalityId):
    try:
        identifier = STAE_URI + municipalityId + '/bike_lanes'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"

@memory.cache
@to_dataframe
def fetch_traffic_jams(municipalityId):
    try:
        identifier = STAE_URI + municipalityId + '/traffic_jams'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"

@memory.cache
@to_dataframe
def fetch_lights(municipalityId):
    try:
        identifier = STAE_URI + municipalityId + '/lights'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"

@memory.cache
@to_dataframe
def fetch_murals(municipalityId):
    try:
        identifier = STAE_URI + municipalityId + '/murals'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"

@memory.cache
@to_dataframe
def fetch_parks(municipalityId):
    try:
        identifier = STAE_URI + municipalityId + '/parks'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"

@memory.cache
@to_dataframe
def fetch_parcels(municipalityId):
    try:
        identifier = STAE_URI + municipalityId + '/parcels'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"

@memory.cache
@to_dataframe
def fetch_zones(municipalityId):
    try:
        identifier = STAE_URI + municipalityId + '/zones'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"

@memory.cache
@to_dataframe
def fetch_transit_routes(municipalityId):
    try:
        identifier = STAE_URI + municipalityId + '/transit_routes'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"

@memory.cache
@to_dataframe
def fetch_transit_vehicles(municipalityId):
    try:
        identifier = STAE_URI + municipalityId + '/transit_vehicles'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"