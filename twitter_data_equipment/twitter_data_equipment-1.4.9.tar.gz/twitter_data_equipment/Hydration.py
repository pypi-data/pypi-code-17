"""
This module helps hydrating a file containing a list of tweet-ids. It gets the file with the tweet-ids as input
and produces a Json-File as output.
"""

from twarc import Twarc
import json




def hydrate_file(input_path, output_path, key_dict):
    """
    This function gets a file with tweet-ids, an ouput-path for the Json-File and a dict containing the 
    twitter-credentials as input, and produces a Json-File containing the hydrated tweets.
    The method is based on the library 'Twarc' and the call to the method 'Twarc.hydrate'
    
    :param str input_path: The path leading to the input-file. The input-file must have a header and then contain a tweet-id one at a line.
    
    :param str output_path: The path leading to the output-file. The output-file gets generated if not existent and overwriten if existent.
    
    :param dict of (str,str) key_dict: The key_dict must contain for keys containing the twitter login information and be of the following form:
    {
    'consumer_key':'<consumer_key>',
    'consumer_secret':'<consumer_secret>',
    'access_token':'<access_token>',
    'access_token_secret':'<access_token_secret>'
    }
    
    """
    i = open(input_path)
    t = Twarc(key_dict['consumer_key'], key_dict['consumer_secret'], key_dict['access_token'],
              key_dict['access_token_secret'])
    with open(output_path, 'w') as outfile:
        for tweet in t.hydrate(i):
            outfile.write(json.dumps(tweet) + '\n')

