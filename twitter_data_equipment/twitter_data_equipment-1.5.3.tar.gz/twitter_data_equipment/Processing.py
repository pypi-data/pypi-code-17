#!/usr/bin/env python

"""
Module processes Json-Files that were generated with e.g. Hydration.hydrate_file containing one tweet per line. 
The information gets cleaned and processed such that it can be read and transformed via the pandas-library.
"""

import json
import logging
import re
import os
from datetime import datetime
import pytz


def process_tweets(input_path, output_path):
    """
    Takes input-path of file in Json-Format containing on each line information for exactly one tweet and transforms it
    to Csv-File containing only the relevant data. It contains the following headers:
    
    lang - Language of tweet
    
    created_at - Date of creation of tweet
    
    rt_count - Number of times retweeted
    
    fav_count - Number of times this tweet has been liked
    
    t_id - tweet id
    
    statuses_count - Number of tweets tweeted by the user 
    
    profile_fav_count - Number of times the users profile has been liked
    
    followers_count - Amount of followers
    
    friends_count - Amount of friends
    
    listed_count - Number of public lists this user is member of
    
    screen_name - Screen name of user
    
    u_id - User identification number
    
    is_geo - Does tweet contain geo-information? (1: true, 0: false)
    
    geo_lat - Longitude of coordinate

    geo_long - Latitude of coordinate
    
    is_reply - Is tweet a reply? (1: true, 0: false)
    
    in_reply_to_screen_name - Screen name of user who's tweet this tweet was replying to
    
    in_reply_to_status_id - Identification number of tweet this tweet was replying to
    
    in_reply_to_user_id_str - Identifation number string of tweet this tweet was replying to
    
    RT - Is tweet a retweet? (1: true, 0: false)
    
    r_id - Identification number of retweeted (original) tweet 
    
    r_screen_name - Screen name of user whos tweet has been retweeted
    
    r_uid - User identification number of user whos tweet has been retweeted
    
    QT - Is tweet a quote of another tweet? (1: true, 0: false)
    
    q_id - Identification number of quoted (original) tweet
    
    q_screen_name - Screen name of user whos tweet has been quoted
    
    q_uid - User identification number of user whos tweet has been quoted
    
    hashtags - Used hashtags
    
    usermentions - Mentioned users
    
    urls - Contained Urls
    
    media - Does tweet contain Urls leading to media files? (1: true, 0: false)
    
    mediaurls - Contained Urls leading to media-files
    
    text - Tweet text
    
    :param str input_path: Path to Json-File containing tweet information
    
    :param str output_path: Path to destination of Csv-File
    
    """

    # Define Statistic Values
    lineNum = 1
    deleted_tweet_count = 0
    wrong_lang = 0
    lastid = "None"

    # Open input and output-file
    i = open(input_path)
    o = open(output_path, 'w')

    # Set up logger
    dir_name, _ = os.path.splitext(output_path)
    logger = logging.getLogger(dir_name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("{0}.log".format(dir_name), mode='w')
    fh.setLevel(logging.INFO)
    fh_format = logging.Formatter('%(asctime)s, %(message)s')
    fh.setFormatter(fh_format)
    logger.addHandler(fh)

    # Write header of log-file
    fh.setFormatter(logging.Formatter('%(message)s'))
    logger.info("time,is_deleted,tweet_id,deleted_tweet_user_id")
    fh.setFormatter(logging.Formatter('%(asctime)s,%(message)s'))
    header = "lang,created_at,rt_count,fav_count,t_id,statuses_count,profile_fav_count"
    header += ",followers_count,friends_count,listed_count,screen_name,u_id"
    header += ",is_geo,geo_lat,geo_long"
    header += ",is_reply,in_reply_to_screen_name,in_reply_to_status_id,in_reply_to_user_id_str"
    header += ",RT,r_id,r_screen_name,r_uid"
    header += ",QT,q_id,q_screen_name,q_uid"
    header += ",hashtags,usermentions,urls"
    header += ",media,mediaurls"
    header += ",text"
    o.write(header + '\n')
    o.flush()

    # Iterate through input-file and extract the wanted information, print it to output-file in csv-wise manner
    for line in i.readlines():
        tweet = json.loads(line)
        if 'delete' in tweet:
            logger.info("1," + tweet['delete']['status']['id_str'] + "," + tweet['delete']['status']['user_id_str'])
            deleted_tweet_count = deleted_tweet_count + 1
        else:
            if tweet['lang'] != "en":
                wrong_lang = wrong_lang + 1
            else:
                pstr = tweet['lang']
                pstr += "," + str(datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC))
                pstr += "," + str(tweet['retweet_count'])
                pstr += "," + str(tweet['favorite_count'])
                pstr += "," + tweet['id_str']
                pstr += "," + str(tweet['user']['statuses_count'])
                pstr += "," + str(tweet['user']['favourites_count'])
                pstr += "," + str(tweet['user']['followers_count'])
                pstr += "," + str(tweet['user']['friends_count'])
                pstr += "," + str(tweet['user']['listed_count'])
                pstr += "," + tweet['user']['screen_name']
                pstr += "," + tweet['user']['id_str']

                if tweet['coordinates'] is not None and tweet['coordinates']['type'] == 'Point':
                    pstr += ',1,' + str(tweet['coordinates']['coordinates'][1]) + "," + str(
                        tweet['coordinates']['coordinates'][0])
                elif tweet['coordinates'] is None and tweet['place'] is not None:
                    if tweet['place']['bounding_box'] is not None:
                        coordinates = tweet['place']['bounding_box']['coordinates'][0]
                        longitude = (int(coordinates[0][0]) + int(coordinates[1][0]) + int(coordinates[2][0]) + int(
                            coordinates[3][0])) / 4
                        latitude = (int(coordinates[0][1]) + int(coordinates[1][1]) + int(coordinates[2][1]) + int(
                            coordinates[3][1])) / 4
                        pstr += ',1,' + str(latitude) + "," + str(longitude)
                elif tweet['coordinates'] is None and tweet['place'] is None:
                    pstr += ',0,,'

                if tweet['in_reply_to_status_id_str'] is None:
                    pstr += ',0,,,'
                else:
                    pstr += ",1" + "," + str(tweet['in_reply_to_screen_name']) + "," + str(
                        tweet['in_reply_to_status_id_str']) + "," + str(tweet['in_reply_to_user_id_str'])

                if 'retweeted_status' in tweet:
                    pstr = pstr + ",1," + tweet['retweeted_status']['id_str']
                    pstr += "," + tweet['retweeted_status']['user']['screen_name']
                    pstr += "," + tweet['retweeted_status']['user']['id_str']
                else:
                    pstr = pstr + ",0,,,"
                if 'quoted_status' in tweet:
                    pstr = pstr + ",1," + tweet['quoted_status']['id_str']
                    pstr += "," + tweet['quoted_status']['user']['screen_name']
                    pstr += "," + tweet['quoted_status']['user']['id_str']
                else:
                    pstr = pstr + ",0,,,"

                hashtags = [a['text'] for a in tweet['entities']['hashtags']]
                usermentions = [a['id_str'] for a in tweet['entities']['user_mentions']]
                urls = [a['expanded_url'] for a in tweet['entities']['urls'] if a['expanded_url'] != 'null']
                urls = [re.sub("\b[']\b'", string=a, repl='') for a in urls]
                urls = str(urls).replace('"', "'")
                pstr = pstr + ',"' + str(hashtags) + '","' + str(usermentions) + '","' + str(urls) + '"'
                if 'media' in tweet['entities']:
                    mediaurls = [media['media_url'] for media in tweet['entities']['media']]
                    mediaurls = [re.sub("\b[']\b'", string=a, repl='') for a in mediaurls]
                    mediaurls = str(mediaurls).replace('"', "'")
                    pstr += ',1,"' + str(mediaurls) + '"'
                else:
                    pstr += ',0,'
                tweet_text = tweet['text'].replace('\n', ' ').replace('\r', '')
                tweet_text = tweet_text.replace('"', "'")
                pstr += ',"' + tweet_text + '"'
                pstr.encode('utf8')
                lastid = tweet['id_str']
                o.write(pstr + '\n')
                o.flush()
                lineNum += 1

    # Write Summary to logfile
    fh.setFormatter(logging.Formatter('%(message)s'))
    logger.info("\n")
    logger.info("----------------------------------------------------------------")
    logger.info("\n")
    logger.info("Summary")
    logger.info("Total Tweets Processed (Input): " + str(lineNum - 1))
    logger.info("Total Tweets Processed (Output): " + str((lineNum - 1) - (deleted_tweet_count + wrong_lang)))
    logger.info("Total Deleted Tweets: " + str(deleted_tweet_count))
    logger.info("Wrong Language Tweets: " + str(wrong_lang))
    logger.info("Last Hydrated Tweet ID: " + str(lastid))
    logging.shutdown()

