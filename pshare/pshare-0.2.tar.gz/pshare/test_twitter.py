# Author: Brandon Powers
# Purpose:
#     - Contains the unit tests for the
#     'Twitter' class

import unittest
import tweepy
import tweet
from twitter import Twitter
from argparse import Namespace

# Disables two warnings when pshare is run
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

class TestTwitter(unittest.TestCase):
    def setUp(self):
        # simulate "psh -t read" command args
        args = Namespace(cargs='home', command='read', facebook=False, media='', number=10, status='', twitter=True, verbose=False)
        self.t = Twitter(args)
        self.t.login()

    def test_login(self):
        # Tests login() & indirectly, known_user_auth()
        # and first_time_auth() by checking the access
        # token of 'self.auth'

        # read in access token from 'twitter-access-token.txt'
        with open('twitter-access-token.txt', 'r') as infile:
            content = infile.readlines()
        access_token = content[0].rstrip()
        access_token_secret = content[1].rstrip()
        self.assertEqual(self.t.auth.access_token, access_token)
        self.assertEqual(self.t.auth.access_token_secret, access_token_secret)

    def test_get_tweepy_API(self):
        # Tests get_tweepy_API & verify() indirectly

        self.assertFalse(isinstance(self.t.api, tweepy.API))
        self.t.get_tweepy_API()
        self.assertTrue(isinstance(self.t.api, tweepy.API))

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
