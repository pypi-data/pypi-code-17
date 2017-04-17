import pandas as pd
import requests
import time

class Geocoder(object):
    
    def __init__(self, API_KEY=None):
        self.API_KEY = API_KEY
        
    
    
    def geocode(self, address):

        """
        Geocode results from Google Maps Geocoding API.

        @param address: String with address to search. Make as accurate as possible. For Example "18 Grafton Street, Dublin, Ireland"
        @param api_key: String API key if present from google. 
                        If supplied, requests will use your allowance from the Google API. If not, you
                        will be limited to the free usage of 2500 requests per day.
        Output: Geocoded Result,
        """
        
        print "currently searching for: {}".format(address)

        # Init Geocoding url
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)
        
        # Link API Key if applicable
        if self.API_KEY is not None:
            geocode_url = geocode_url + "&key={}".format(self.API_KEY)

        # Ping google for the reuslts:
        results = requests.get(geocode_url)
        # Convert JSON resultsto dict using requests
        results = results.json()
        
        # base case
        if (len(results['results']) == 0) and (len(address.split()) == 1):
            output = {
                "formatted_address" : None,
                "latitude": None,
                "longitude": None,
                "accuracy": None,
                "google_place_id": None,
                "type": None,
                "postcode": None,
                'input_string': address,
                'status': results.get('status')
            }
            return output

        # if there's no results or an error, try for smaller subset of string
        elif len(results['results']) == 0:
            addy = " ".join(address.split()[1:len(address.split())])
            return self.geocode(addy)

        # result found - return results
        else:    
            answer = results['results'][0]
            output = {
                "formatted_address" : answer.get('formatted_address'),
                "latitude": answer.get('geometry').get('location').get('lat'),
                "longitude": answer.get('geometry').get('location').get('lng'),
                "accuracy": answer.get('geometry').get('location_type'),
                "type": ",".join(answer.get('types')),
                "postcode": ",".join([x['long_name'] for x in answer.get('address_components') 
                                      if 'postal_code' in x.get('types')]),
                'input_string': address,
                'status': results.get('status')
            }

            return output
    