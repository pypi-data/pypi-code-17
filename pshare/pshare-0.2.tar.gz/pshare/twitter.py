# Author: Brandon Powers
# Purpose:
#     - 'Twitter' is a class that implements the
#     actions specified by the -t flag in pshare

import sys
from tweet import Tweet
import tweepy
import os.path

# initializing authentication -- consumer info is hidden in local directory, not on GitHub for security purposes -- ask for use
CONSUMER_KEY = 'xopCIjkuJk5FJupf653EAI9Am'
CONSUMER_SECRET = 'X7BVFS7GCYIUzsvQE6JuiFTnFnPPvDy954UUVb6HxOF0MAXXlH'
ACCESS_KEY = ''
ACCESS_SECRET = ''

class Twitter:
    def __init__(self, args):
        # Initializes the instance variables of a Twitter instance:
        #     auth -> OAuth object used to gain access to tweepy API
        #     filename -> Location of access token info (if it exists)
        #     api -> Holds the tweepy API object
        #     args -> Command-line args used to execute commands {read, post, del}

        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.filename = 'twitter-access-token.txt'
        self.api = ''
        self.args = args
        
    def login(self):
        # User login by attaching the access token to 'self.auth'

        access_token_exists = os.path.isfile(self.filename)
        if access_token_exists: 
            self.known_user_auth()
        else:
            self.first_time_auth()

    def known_user_auth(self):
        # Reads the access token (first line = key, second line = secret)
        # from 'self.filename' & adds it to 'self.auth'

        # first line is TWITTER_ACCESS_KEY, second line is TWITTER_ACCESS_SECRET <-- reason for hardcoded indices
        with open(self.filename, 'r') as infile:
            access_token = infile.readlines()
            ACCESS_KEY = str(access_token[0]).rstrip('\n')
            ACCESS_SECRET = str(access_token[1])
        self.auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    def first_time_auth(self):
        # Asks user to authorize pshare by requesting an access token, 
        # then stores access token in a local file & adds it to 'self.auth'

        try:
            print '**Initial authentication required for first-time user**'
            print '(1) Open the following URL in a web browser: ' + str(self.auth.get_authorization_url())
            print '(2) Authorize pshare to post to + read from your Twitter account'
            verifier = raw_input('(3) Input the access code Twitter redirects you to here: ')
            print '(4) Getting access token...'
            self.auth.get_access_token(verifier)
            print '(5) Storing access token information in file "twitter-access-token.txt" for future use'
            with open(self.filename, 'w') as outfile:
                outfile.write('{}\n{}'.format(self.auth.access_token, self.auth.access_token_secret))
        except tweepy.TweepError:
            print 'pshare.py: error: failed to get request token OR access token.'

    def get_tweepy_API(self):
        # Initialize & verify tweepy API credentials, stored in 'self.api'

        print 'Authenticating credentials...'
        self.api = tweepy.API(self.auth)
        self.verify()

    def verify(self):
        # Verify tweepy API credentials

        try:
            if self.api.verify_credentials():
                print 'Verified authentication credentials -- gained access to Twitter API'
        except tweepy.TweepError:
            print 'pshare.py: error: credentials are invalid: delete "twitter-access-token.txt" & re-authenticate'
            sys.exit(1)

    def read(self):
        # Execute a read command, using the args specified in 'self.args'

        statuses = []
        if self.args.cargs == 'home':
            statuses = self.api.home_timeline(count=self.args.number)
        elif self.args.cargs == 'user':
            statuses = self.api.user_timeline(count=self.args.number)
        tweets = self.statuses_to_tweets(statuses)
        print '\n**Top {} tweets on your timeline**\n'.format(str(self.args.number))
        for tweet in tweets:
            tweet.display(self.args.verbose)
    
    def statuses_to_tweets(self, statuses):
        # Given a list of status objects, extract only the necessary info
        # & return a list of Tweet objects -- helper method for read()

        tweets = []
        for status in statuses:
            name = status.user.name.encode('utf-8')
            screen_name = str(status.user.screen_name)
            text = status.text
            created_at = status.created_at
            id_num = status.id
            tweets.append(Tweet(name, screen_name, text, created_at, id_num))
        return tweets

    def post(self):
        # Execute a post command, using the args specified in 'self.args'

        try:
            # tweet media with cargs as text | tweet cargs as text, no media
            if not self.args.cargs == 'home' and self.args.media:
                self.api.update_with_media(self.args.media, self.args.cargs)
            elif not self.args.cargs == 'home':
                self.api.update_status(self.args.cargs)

            # tweet media with status file contents as text
            elif self.args.media and self.args.status:
                status = ''
                with open(self.args.status, 'r') as infile:
                    status = infile.read()
                self.api.update_with_media(self.args.media, status) 

            # only media file -- tweet media
            elif self.args.media:
                self.api.update_with_media(args.media)

            # only status file -- tweet contents
            elif self.args.status:
                status = ''
                with open(self.args.status, 'r') as infile:
                    status = infile.read()
                self.api.update_status(status)

            # prompt user -- no cargs, media, or status file
            else:
                status = raw_input('Enter tweet to post: ')
                self.api.update_status(status)
        
        except tweepy.TweepError:
            print 'pshare.py: error: tweet was over 140 characters OR encountered a post error' 
            sys.exit(1)

    def delete(self):
        # Execute a del command, using the args specified in 'self.args'

        try:
            self.api.destroy_status(self.args.cargs)
            print 'Deleted tweet with id #: {}'.format(str(self.args.cargs))
        except tweepy.TweepError:
            print 'pshare.py: error: tweet id # is invalid OR delete failed' 
            sys.exit(1)
