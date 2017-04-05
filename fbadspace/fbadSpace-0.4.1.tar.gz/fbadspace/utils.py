from facebookads.objects import (AdUser, Campaign, AdSet)
from facebookads.adobjects import adaccount
from facebookads.adobjects.campaign import Campaign
from facebookads.adobjects.targetingsearch import TargetingSearch
from facebookads.exceptions import FacebookRequestError

import requests


def activateCampaign(campaign):
    params = {
        Campaign.Field.status : Campaign.Status.active
    }
    response = campaign.api_update(params=params)
    return response


def pauseCampaign(campaign):
    params = {
        Campaign.Field.status : Campaign.Status.paused
    }
    response = campaign.api_update(params=params)
    return response


def getInterestsByKeyword(keyword):
    params ={
        'q': keyword,
        'type': 'adinterest'
    }
    resp = TargetingSearch.search(params=params)
    return resp


def getInterestSuggestionByInterestList(keywords):
    params = {
    'type': 'adinterestsuggestion',
    'interest_list': keywords,
    }
    resp = TargetingSearch.search(params=params)
    return resp


def getAllCategories():
    params = {
        'type': 'adTargetingCategory',
        'class': 'interests',
    }
    resp = TargetingSearch.search(params=params)
    return resp


def getCategoriesByLevel(level):
    interests = getAllCategories()
    results = []
    for inter in interests:
        if len(inter['path']) == level:
            results.append(inter)
    return results


def validateInterests(keywords, api=None):
    params = {
        'type': 'adinterestvalid',
        'interest_list': keywords
    }
    return TargetingSearch.search(params=params, api=api)


def validateInterestsById(ids, api=None):
    params = {
        'type': 'adinterestvalid',
        'interest_fbid_list': ids
    }
    return TargetingSearch.search(params=params, api=api)


def getInterests(keywords):
    interests = []
    #comprobamos si alguna keyword es un interes en si misma
    for respInterest in validateInterests(keywords):
        if respInterest['valid'] == True:
            interests.append({'id': respInterest['id'], 'name': respInterest['name']})
    for kw in keywords:
        for targeting in getInterestsByKeyword(kw):
            interests.append({'id': targeting['id'], 'name': targeting['name']})
    suggestedInterests = getInterestSuggestionByInterestList([intr['name'] for intr in interests])
    for intr in suggestedInterests:
        interests.append({'id': intr['id'], 'name': intr['name']})
    return interests


def getCurrentAccountId(api=None):
    return AdUser(fbid='me', api=api).remote_read()['id']


def long_lived_token(app_id, app_secret, access_token):
    url = 'https://graph.facebook.com/oauth/access_token'
    queryparams = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': access_token
    }
    resp = requests.get(url, params=queryparams)

    if resp.status_code != 200:
        raise NotImplementedError('Error exchanging access_token')

    try:
        json_resp = resp.json()

        if 'error' in json_resp or not 'access_token' in json_resp:
            raise NotImplementedError(json_resp.get('message', 'Error from Facebook oauth long lived token'))

    except (ValueError, NotImplementedError):
        raise

    return json_resp['access_token']

