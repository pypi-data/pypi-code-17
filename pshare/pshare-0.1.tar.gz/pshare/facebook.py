# Author: Matt Grant
# Purpose:
#     - 'Facebook' is a class that implements the
#     actions specified by the -f flag in pshare

import sys
import facepy
from facepy import GraphAPI
import os.path

# initializing authentication -- consumer info is hidden in local directory, not on GitHub for security purposes -- ask for use
APPLICATION_ID = '190191088163549'
APPLICATION_SECRET = '830886c7f6d51dceea255f8b258a339b'

class Facebook:
    def __init__(self, args):
    	print('Facebook init')
    	graph = GraphAPI('access token')
    	friends = graph.get('me/friends/')
    	print(friends)

    def login(self):
    	print("Facebook login")

    def known_user_auth(self):
    	print("Facebook known_user_auth")
    	
    def first_time_auth(self):
    	print("Facebook first_time_auth")
    	
    def get_facepy_API(self):
    	print("Facebook get_facepy_API")
    	
    def verify(self):
    	print("Facebook verify")
    	
    def read(self):
        print("Facebook read")
    	
    def statuses_to_tweets(self, statuses):
    	print("Facebook statuses_to_tweets")
    	
    def post(self):
    	print("Facebook post")
    	
    def delete(self):
    	print("Facebook delete")
    	