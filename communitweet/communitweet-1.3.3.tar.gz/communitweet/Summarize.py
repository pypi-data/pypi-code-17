"""
Module for calculating various percentages as well as the top X entries of 
hashtags, users, urls, media and locations that appear in a dataframe
"""

from collections import Counter


def get_top_n_hashtags(n_positions, dataframe, give_freq=False):
    """
    Returns the most used hashtags in the given dataframe, amount is specified in the n_n_positions parameter,
    and the give_freq parameter specifies whether the frequency of each hashtag should be returned.
    
    :param int n_positions: Number of most used hashtags should be returned. E.g. Top 10 or Top 5, if -1 is given, all
    hashtags get returned
    
    :param pd.Dataframe dataframe: Dataframe containing twitter data
    
    :param boolean give_freq: Whether to return the frequency or not
    
    :return list: Containing the specified amount(all if n_positions==-1) of hashtags either including their exact 
    frequency or not 
    
    """
    df = dataframe[dataframe.hashtags != '[]']
    hashtag_list = list()
    for row in df.itertuples():
        try:
            hashtags = eval(row.hashtags)
            for hashtag in hashtags:
                hashtag_list.append(hashtag)
        except:
            pass
    hashtags_to_freq = dict(Counter(hashtag_list))
    sorted_hash_freq = sorted(hashtags_to_freq.items(), key=lambda x: x[1], reverse=True)
    if give_freq:
        if n_positions == -1:
            return sorted_hash_freq
        else:
            return sorted_hash_freq[0:n_positions]
    else:
        if n_positions == -1:
            return [x[0] for x in sorted_hash_freq]
        else:
            return [x[0] for x in sorted_hash_freq[0:n_positions]]


def get_top_n_users(n_positions, dataframe, give_freq=False):
    """
    Returns the most active users (measured on how many tweets they tweeted) in the given dataframe, 
    amount is specified in the n_n_positions parameter and the give_freq parameter specifies whether the frequency of 
    each hashtag should be returned.

    :param int n_positions: Number of most active user should be returned. E.g. Top 10 or Top 5, if -1 is given, all users
    get returned

    :param pd.Dataframe dataframe: Dataframe containing twitter data

    :param boolean give_freq: Whether to return the frequency or not

    :return list: Containing the specified amount(or all if n_positions==-1) of users either including their exact frequency or not 

    """
    users_list = list()
    for row in dataframe.itertuples():
        user = row.u_id
        name = row.screen_name
        users_list.append((user, name))

    users_to_freq = dict(Counter(users_list))
    sorted_users_freq = sorted(users_to_freq.items(), key=lambda x: x[1], reverse=True)
    if give_freq:
        if n_positions == -1:
            return sorted_users_freq
        else:
            return sorted_users_freq[0:n_positions]
    else:
        if n_positions == -1:
            return [x[0] for x in sorted_users_freq]
        else:
            return [x[0] for x in sorted_users_freq[0:n_positions]]


def get_top_n_urls(n_positions, dataframe, give_freq=False):
    """
    Returns the most tweeted urls in the given dataframe, amount is specified in the n_n_positions parameter 
    and the give_freq parameter specifies whether the frequency of each url should be returned.

    :param int n_positions: Number of most tweeted url should be returned. E.g. Top 10 or Top 5, if -1 is given, all urls
    get returned

    :param pd.Dataframe dataframe: Dataframe containing twitter data

    :param boolean give_freq: Whether to return the frequency or not

    :return list: Containing the specified amount(or all if n_positions==-1) of urls either including their exact frequency or not 

    """
    df = dataframe[dataframe.urls != '[]']
    urls_list = list()
    for row in df.itertuples():
        try:
            urls = eval(row.urls)
            for url in urls:
                urls_list.append(url)
        except:
            pass

    urls_to_freq = dict(Counter(urls_list))
    sorted_urls_freq = sorted(urls_to_freq.items(), key=lambda x: x[1], reverse=True)
    if give_freq:
        if n_positions == -1:
            return sorted_urls_freq
        else:
            return sorted_urls_freq[0:n_positions]
    else:
        if n_positions == -1:
            return [x[0] for x in sorted_urls_freq]
        else:
            return [x[0] for x in sorted_urls_freq[0:n_positions]]


def get_top_n_media(n_positions, dataframe, give_freq=False):
    """
    Returns the most tweeted media-urls in the given dataframe, 
    amount is specified in the n_n_positions parameter and the give_freq parameter specifies whether the frequency of 
    each media-url should be returned.

    :param int n_positions: Number of most tweeted media-urls should be returned. E.g. Top 10 or Top 5, if -1 is given, all media-urls
    get returned

    :param pd.Dataframe dataframe: Dataframe containing twitter data

    :param boolean give_freq: Whether to return the frequency or not

    :return list: Containing the specified amount(or all if n_positions==-1) of media-urls either including their exact frequency or not 

    """
    df = dataframe[dataframe.media == 1]
    media_url_list = list()
    for row in df.itertuples():
        try:
            medias = eval(row.mediaurls)
            for media in medias:
                media_url_list.append(media)
        except:
            pass

    media_to_freq = dict(Counter(media_url_list))
    sorted_mediaurls_freq = sorted(media_to_freq.items(), key=lambda x: x[1], reverse=True)
    if give_freq:
        if n_positions == -1:
            return sorted_mediaurls_freq
        else:
            return sorted_mediaurls_freq[0:n_positions]
    else:
        if n_positions == -1:
            return [x[0] for x in sorted_mediaurls_freq]
        else:
            return [x[0] for x in sorted_mediaurls_freq[0:n_positions]]


def get_top_n_locations(n_positions, dataframe, unit_of_location='States', give_freq=False):
    """
    Returns the most geo-locations that tweets where sent from in the given dataframe, 
    amount is specified in the n_n_positions parameter and the give_freq parameter specifies whether the frequency of 
    each location should be returned.

    :param int n_positions: Number of most geo-locations that tweets where sent from should be returned. E.g. Top 10 or Top 5, if -1 is given, all
    locations get returned

    :param pd.Dataframe dataframe: Dataframe containing twitter data
    
    :param str unit_of_location: The basic geographic unit that is taken to identify wheter to tweets were tweeted from the same place or not

    :param boolean give_freq: Whether to return the frequency or not

    :return list: Containing the specified amount(or all if n_positions==-1) of Locations either including their exact frequency or not 

    """
    if 'has_stats' in dataframe:
        df = dataframe[dataframe.has_stats == 1]
        state_fips_list = list()
        if len(df) > 0:
            for row in df.itertuples():
                try:
                    if unit_of_location == 'States':
                        fips = int(row.State_FIPS)
                        name = str(row.State_Name)
                    elif unit_of_location == 'Counties':
                        fips = int(row.County_FIPS)
                        name = str(row.County_Name)
                except Exception as e:
                    pass
                state_fips_list.append((fips, name))
            state_fips_to_freq = dict(Counter(state_fips_list))
            sorted_state_fips_freq = sorted(state_fips_to_freq.items(), key=lambda x: x[1], reverse=True)
            if give_freq:
                if n_positions == -1:
                    return sorted_state_fips_freq
                else:
                    return sorted_state_fips_freq[0:n_positions]
            else:
                if n_positions == -1:
                    return [x[0][1] for x in sorted_state_fips_freq]
                else:
                    return [x[0][1] for x in sorted_state_fips_freq[0:n_positions]]
        else:
            return []
    else:
        return []


def get_perc_of_geo_info(dataframe):
    """
    Calculates the percentage of all tweets in the given dataframe that contain geo-info
    
    :param pd.Dataframe dataframe: Dataframe containing twitter data
    
    :return: Either string telling the error or integer telling the percentage
    
    """
    if 'is_geo' in dataframe:
        df_geo = dataframe[dataframe.is_geo == 1]
        if len(df_geo) > 0:
            return round(len(df_geo) / len(dataframe) * 100, 1)
        else:
            return 'No geographical Information in dataset'
    else:
        return 'No geographical Information in dataset'


def get_perc_of_stats_info(dataframe):
    """
    Calculates the percentage of all tweets in the given dataframe that contain demographical information

    :param pd.Dataframe dataframe: Dataframe containing twitter data

    :return: Either string telling the error or integer telling the percentage

    """
    if 'has_stats' in dataframe:
        df_stats = dataframe[dataframe.has_stats == 1]
        if len(df_stats) > 0:
            return round(len(df_stats) / len(dataframe) * 100, 1)
        else:
            return 'No demographic statistic in dataset'
    else:
        return 'No demographic statistic in dataset'


def get_perc_of_media(dataframe):
    """
    Calculates the percentage of all tweets in the given dataframe that contain media-urls

    :param pd.Dataframe dataframe: Dataframe containing twitter data

    :return: Either string telling the error or integer telling the percentage

    """
    if 'media' in dataframe:
        df_stats = dataframe[dataframe.media == 1]
        if len(df_stats) > 0:
            return round(len(df_stats) / len(dataframe) * 100, 1)
        else:
            return 'No media in dataframe'
    else:
        return 'No media in dataframe'


def get_perc_of_qt(dataframe):
    """
    Calculates the percentage of all tweets in the given dataframe that are quotes

    :param pd.Dataframe dataframe: Dataframe containing twitter data

    :return: Either string telling the error or integer telling the percentage

    """
    if 'QT' in dataframe:
        df_stats = dataframe[dataframe.QT == 1]
        if len(df_stats) > 0:
            return round(len(df_stats) / len(dataframe) * 100, 1)
        else:
            return 'No quoting in dataset'
    else:
        return 'No quoting in dataset'


def get_perc_of_rt(dataframe):
    """
    Calculates the percentage of all tweets in the given dataframe that are retweets

    :param pd.Dataframe dataframe: Dataframe containing twitter data

    :return: Either string telling the error or integer telling the percentage

    """
    if 'RT' in dataframe:
        df_stats = dataframe[dataframe.RT == 1]
        if len(df_stats) > 0:
            return round(len(df_stats) / len(dataframe) * 100, 1)
        else:
            return 'No retweets in dataset'
    else:
        return 'No retweets in dataset'


def get_perc_of_replies(dataframe):
    """
    Calculates the percentage of all tweets in the given dataframe that are replies

    :param pd.Dataframe dataframe: Dataframe containing twitter data

    :return: Either string telling the error or integer telling the percentage

    """
    if 'is_repy' in dataframe:
        df_stats = dataframe[dataframe.is_reply == 1]
        if len(df_stats > 0):
            return round(len(df_stats) / len(dataframe) * 100, 1)
        else:
            return 'No replies in dataset'
    else:
        return 'No replies in dataset'


def analyze_dataframe(dataframe, give_freq):
    """
    Analyzes the dataframe through application of all specified methods above.
    
    :param pandas.Dataframe dataframe: Dataframe containing twitter data
    
    :param bool give_freq: Whether frequency should be returned or not
    
    :return dict: Containing all information on hashtags, users, media, urls, geo-info and demographic-info
    
    """
    analyze_dict = dict()
    analyze_dict['hashtags'] = get_top_n_hashtags(10, dataframe, give_freq=give_freq)
    analyze_dict['urls'] = get_top_n_urls(10, dataframe, give_freq=give_freq)
    analyze_dict['media'] = get_top_n_media(10, dataframe, give_freq=give_freq)
    analyze_dict['users'] = get_top_n_users(10, dataframe, give_freq=give_freq)
    analyze_dict['state_fips'] = get_top_n_locations(10, dataframe, give_freq=give_freq)
    analyze_dict['geo_perc'] = get_perc_of_geo_info(dataframe)
    analyze_dict['stats_perc'] = get_perc_of_stats_info(dataframe)
    analyze_dict['media_perc'] = get_perc_of_media(dataframe)
    analyze_dict['qt_perc'] = get_perc_of_qt(dataframe)
    analyze_dict['rt_perc'] = get_perc_of_rt(dataframe)
    analyze_dict['reply_perc'] = get_perc_of_replies(dataframe)
    return analyze_dict
