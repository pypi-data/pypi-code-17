import pandas as pd
import requests


def to_dataframe(func):
    def wrapper(municipalityId):
        return pd.DataFrame(func(municipalityId))
    return wrapper


@to_dataframe
def fetch_trips(municipalityId):
    try:
        identifier = 'https://municipal.systems/v1/municipalities/' + municipalityId + '/trips'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"


@to_dataframe
def fetch_issues(municipalityId):
    try:
        identifier = 'https://municipal.systems/v1/municipalities/' + municipalityId + '/issues'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"


@to_dataframe
def fetch_building_permits(municipalityId):
    try:
        identifier = 'https://municipal.systems/v1/municipalities/' + municipalityId + '/building_permits'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"


@to_dataframe
def fetch_businesses(municipalityId):
    try:
    	identifier = 'https://municipal.systems/v1/municipalities/' + municipalityId + '/businesses'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"


@to_dataframe
def fetch_bike_lanes(municipalityId):
    try:
        identifier = 'https://municipal.systems/v1/municipalities/' + municipalityId + '/bike_lanes'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"


@to_dataframe
def fetch_traffic_jams(municipalityId):
    try:
        identifier = 'https://municipal.systems/v1/municipalities/' + municipalityId + '/traffic_jams'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"


@to_dataframe
def fetch_lights(municipalityId):
    try:
        identifier = 'https://municipal.systems/v1/municipalities/' + municipalityId + '/lights'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"


@to_dataframe
def fetch_murals(municipalityId):
    try:
        identifier = 'https://municipal.systems/v1/municipalities/' + municipalityId + '/murals'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"


@to_dataframe
def fetch_parks(municipalityId):
    try:
        identifier = 'https://municipal.systems/v1/municipalities/' + municipalityId + '/parks'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"


@to_dataframe
def fetch_parcels(municipalityId):
    try:
        identifier = 'https://municipal.systems/v1/municipalities/' + municipalityId + '/parcels'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"


@to_dataframe
def fetch_zones(municipalityId):
    try:
        identifier = 'https://municipal.systems/v1/municipalities/' + municipalityId + '/zones'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"


@to_dataframe
def fetch_transit_routes(municipalityId):
    try:
        identifier = 'https://municipal.systems/v1/municipalities/' + municipalityId + '/transit_routes'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"


@to_dataframe
def fetch_transit_vehicles(municipalityId):
    try:
        identifier = 'https://municipal.systems/v1/municipalities/' + municipalityId + '/transit_vehicles'
        r = requests.get(identifier).json()
        return r['results']
    except ValueError:
        print "invalid municipalityId"