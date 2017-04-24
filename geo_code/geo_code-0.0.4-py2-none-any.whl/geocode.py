import pandas as pd
import requests
import time

class Geocoder(object):
    
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY
        
    
    
    def geocode(self, address, string_to_remove='', verbose=True):

        """
        Geocode results from Google Maps Geocoding API.

        @param address: String with address to search. Make as accurate as possible. For Example "18 Grafton Street, Dublin, Ireland"
        @param api_key: String API key if present from google. 
                        If supplied, requests will use your allowance from the Google API. If not, you
                        will be limited to the free usage of 2500 requests per day.
        Output: Geocoded Result,
        """
        address = address.replace(string_to_remove,'')
        
        if verbose:
            #print "currently searching for: {}".format(address)
            pass
        # Set up your Geocoding url
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)
        
        if self.API_KEY is not None:
            geocode_url = geocode_url + "&key={}".format(self.API_KEY)

        # Ping google for the reuslts:
        results = requests.get(geocode_url)
        # Results will be in JSON format - convert to dict using requests functionality
        results = results.json()
        
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

        # if there's no results or an error, return empty results.
        elif len(results['results']) == 0:
            addy = " ".join(address.split()[1:len(address.split())])
            time.sleep(1)
            return self.geocode(addy, string_to_remove='', verbose=verbose)


        else:    
            answer = results['results'][0]
            output = {
                "formatted_address" : answer.get('formatted_address'),
                "latitude": answer.get('geometry').get('location').get('lat'),
                "longitude": answer.get('geometry').get('location').get('lng'),
                "postcode": ",".join([x['long_name'] for x in answer.get('address_components') 
                                      if 'postal_code' in x.get('types')]),
                'input_string': address,
                'status': results.get('status')
            }

            return output
        
    def convert_address_to_list(self, input_csv, address_col, encoding='utf8'):
        """"""
        # Read the data to a Pandas Dataframe
        df = pd.read_csv(input_csv, encoding=encoding)

        if address_col not in df.columns:
            raise ValueError("Missing Address column in input data")

        # Form a list of addresses for geocoding:
        # Make a big list of all of the addresses to be processed.
        addresses = df[address_col].tolist()
            
        return addresses
        
    def geocode_csv(self, input_csv, address_col, output_csv,encoding='utf8', pause_on_rate_limit=True, status_update=10, save_every=2, string_to_remove=''):
        """"""
        addresses = self.convert_address_to_list(encoding=encoding, input_csv=input_csv, address_col=address_col)
        
        # init output list to store results
        results = []
            
        for address in addresses:
            if type(a)
            address = address.replace(string_to_remove,'')
            geocoded = False
                
            #print "Attempting to geocode {}".format(address)
            
            while geocoded is not True:
                    
                try:
                    geocode_res = self.geocode(address, string_to_remove=string_to_remove, verbose=False)
                except Exception as e:
                    #print "Error with {}, Attempt failed".format(address)
                    geocoded = True
                        
                if pause_on_rate_limit:
                    if geocode_res['status'] == 'OVER_QUERY_LIMIT':
                        print "Over Query Limit, Pausing for 30 Minutes"
                        time.sleep(30 * 60)
                        geocode = False
                            
                    else:
                        if geocode_res['status'] != 'OK':
                            #print "Geocode Failed to Locate {}".format(address)
                            pass
                        else:
                            print "Attempt successful"
                        results.append(geocode_res)
                        geocoded = True
                        
                else:
                        if geocode_res['status'] != 'OK':
                            #print "Geocode Failed to Locate {}".format(address)
                            pass
                        else:
                            print "Attempt successful"
                        results.append(geocode_res)
                        geocoded = True
                        
            # print update
            if len(results) % status_update == 0:
                print "###### Completed {} of {} addresses".format(len(results), len(addresses))
                    
            # Save results to csv every `save_every`
            if len(results) % save_every == 0:
                pd.DataFrame(results).to_csv(output_csv, encoding=encoding)
                    
        print
        print "Finished Geocoding"
            
        pd.DataFrame(results).to_csv(output_csv, encoding=encoding)
        
        return results
    
    
        
    def geocode_pandas_df(self, input_df, address_col, output_csv,encoding='utf8', pause_on_rate_limit=True, status_update=10, save_every=50, string_to_remove=''):
        """"""
        
            
        # init output list to store results
        results = []
            
        for address in addresses:
            
            address = address.encode('utf-8', 'ignore').decode('utf-8')
            
            geocoded = False
                
            print "Attempting to geocode {}".format(address)
            
            while geocoded is not True:
                    
                try:
                    geocode_res = self.geocode(address, string_to_remove=string_to_remove)
                    
                except Exception as e:
                    print "Error with {}, Attempt failed".format(address)
                    geocoded = True
                        
                if pause_on_rate_limit:
                    if geocode_res['status'] == 'OVER_QUERY_LIMIT':
                        print "Over Query Limit, Pausing for 30 Minutes"
                        time.sleep(30 * 60)
                            
                else:
                    results.append(geocode_res)
                    print "Attemp successful"
                
            # print update
            if len(results) % status_update == 0:
                print "###### Completed {} of {} addresses".format(len(results), len(addresses))
                    
            # Save results to csv every `save_every`
            if len(results) % save_every == 0:
                pd.DataFrame(results).to_csv(output_csv, encoding=encoding)
                    
        print
        print "Finished Geocoding"
            
        pd.DataFrame(results).to_csv(output_csv, encoding=encoding)
        
        return results
            
    