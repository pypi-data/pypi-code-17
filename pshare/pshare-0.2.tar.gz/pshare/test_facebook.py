# Author: Matt Grant
# Purpose:
#     - Contains the unit tests for the
#     'Facebook' class

import unittest
import facepy
from facebook import Facebook
from argparse import Namespace

# Disables two warnings when pshare is run
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

class TestFacebook(unittest.TestCase):
    def setUp(self):
        # simulate "psh -f read" command args
        args = Namespace(cargs='home', command='read', facebook=True, media='', number=10, status='', twitter=False, verbose=False)
        self.f = Facebook(args)
        self.f.login()

    def test_login(self):
        # Tests login() & indirectly, known_user_auth()
        # and first_time_auth() by checking the access
        # token of 'self.auth'

        # read in access token from 'facebook-access-token.txt'
        with open('facebook-access-token.txt', 'r') as infile:
            content = infile.readlines()
        access_token = content[0].rstrip()
        access_token_secret = content[1].rstrip()
        self.assertEqual(self.f.auth.access_token, access_token)
        self.assertEqual(self.f.auth.access_token_secret, access_token_secret)

    def test_get_facepy_API(self):
        # Tests get_facepy_API & verify() indirectly

        self.assertFalse(isinstance(self.f.api, facepy.API))
        self.f.get_facepy_API()
        self.assertTrue(isinstance(self.f.api, facepy.API))

    def test_statuses_to_tweets(self):
        self.t.get_tweepy_API()
        statuses = self.t.api.home_timeline(count=self.t.args.number)
        tweets = self.t.statuses_to_tweets(statuses)
        # check first element, assume the rest are the same
        self.assertTrue(isinstance(tweets[0], tweet.Tweet))

        tweets = self.t.statuses_to_tweets([])
        self.assertFalse(tweets)

if __name__ == '__main__':
    unittest.main()
