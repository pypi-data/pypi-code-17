"""
Unshortens URls of a given Csv-file with the headers 'url' and 'mediaurl'.
Twitter API is documented here: https://dev.twitter.com/overview/api/tweets
It will create a additional logfile in ~/your_directory/input.log
"""

import requests
import logging
import os
import pandas
import numpy as np



# Define Statistic Values
lineNum = 1
deleted_tweet_count = 0
failed_urls = set()
lastid = "None"
urls_dict = dict()


def _unshorten_url(url, tweet_id, logger, timeout=5):
    """
    Takes a url and follows it until redirecting ends or the specified timeout is over.
    The parameters 'tweet_id' and 'logger' are for logging purposes only.
    To save time,every successful unshortening will be stored in a dict for later re-use of shortened-url
    
    :param str url: The url to be unshortened if possible
    
    :param str tweet_id: The tweet_id of tweet containing url
    
    :param logging.Logger logger: The logger that logs all failed urls
    
    :param int timeout: Amount of seconds for url to respond
    
    :return: returns a url as string
    
    """
    if url in urls_dict.keys():
        return urls_dict[url]
    else:
        try:
            answer = requests.head(url, allow_redirects=True, **{'timeout': timeout}).url
            urls_dict[url] = answer
            return answer
        except Exception:
            logger.info(str(tweet_id) + "," + str(url))
            urls_dict[url] = url
            failed_urls.add(url)
            return url


def unshorten_urls(input_path, output_path, timeout = 5):
    """
    Main function of the module 'Unshortening'. Takes path to a Csv-file coming from the module 'Processing' and the
    path for the output-file.
    
    :param str input_path: Path to input Csv-File
    
    :param str output_path: Path to destination of output Csv-File containing the unshortened urls
    
    :param int timeout: Specify the timeout for the __unshorten_url function
        
    """

    #Setting up the logger
    dir_name, _ = os.path.splitext(output_path)
    logger = logging.getLogger(dir_name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("{0}.log".format(dir_name), mode='w')
    fh.setLevel(logging.INFO)
    fh_format = logging.Formatter('%(asctime)s, %(message)s')
    fh.setFormatter(fh_format)
    logger.addHandler(fh)
    fh.setFormatter(logging.Formatter('%(message)s'))
    logger.info("time,tweet_id, failed_url")
    fh.setFormatter(logging.Formatter('%(asctime)s, %(message)s'))

    #Opening the input and the output-paths
    f = open(input_path)

    #Read the Csv-File
    df = pandas.read_csv(f)

    #Iterate over all rows containing urls and try to unshorten them. If successfull replace the old urls with the new
    #unshortened urls.
    for i, row in df.iterrows():
        try:
            n_urls = eval(row.urls)
            urls_temp = [_unshorten_url(a, row['t_id'], logger,timeout=timeout) for a in n_urls if len(n_urls) != 0]
            df.set_value(i, 'urls', repr(urls_temp))

            if row.media != 0:
                n_mediaurls = eval(row.mediaurls) if not pandas.isnull(row.mediaurls) else []
                mediaurls_temp = [_unshorten_url(a, row['t_id'], logger,timeout=timeout) for a in n_mediaurls if len(n_mediaurls) != 0]
                df.set_value(i, 'mediaurls', repr(mediaurls_temp))
            else:
                df.set_value(i, 'mediaurls', np.nan)
        except SyntaxError:
            pass

    #Write unshortened dataframe to Csv-File again.
    o = open(output_path, 'w')
    df.to_csv(o, mode='w', index=False)

    #Write logger summary on amount of failed urls
    fh.setFormatter(logging.Formatter('%(message)s'))
    logger.info("\n")
    logger.info("----------------------------------------------------------------")
    logger.info("\n")
    logger.info("Summary")
    logger.info("Failed urls: " + str(len(failed_urls)))
    logging.shutdown()
