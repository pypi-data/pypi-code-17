#-*- coding: utf-8 -*-
"""
@file
@brief Call to Cognitive Services.
"""
import http.client
import urllib.request
import urllib.parse
import urllib.error
import json
from .mokadi_exceptions import CognitiveException


def bytes2python(answer):
    """
    Converts JSON bytes into a dictionary.

    @param      answer      bytes
    @return                 any type
    """
    string = answer.decode('utf-8')
    json_obj = json.loads(string)
    return json_obj


def call_api_news(subscription_key, query, market="fr-FR", count=10, offset=0):
    """
    Retrieve resuls for news.

    @param      subscription_key
    @param      query               query
    @param      market              market
    @param      count               number of results
    @param      offset              skip results
    @return                         results

    Example of a result:

    ::

        {'_type': 'News',
         'readLink': 'https://api.cognitive.microsoft.com/api/v5/news/search?q=',
         'value': [{'name': "Colombie : le bilan de la coulée de boue s'alourdit 54 morts",
                    'url': 'http://www.bing.com/cr?IG=CEFF9C63FD7A4439B591261606484860&CID=3B75F5FD9A146DBF103CFFA49BF36C83&rd=1&',
                    'image': {'thumbnail': {'contentUrl': 'https://www.bing.com/th?id=ON.08357B50C029DBC09D053826F9B22658&pid=News',
                                            'width': 700, 'height': 304}},
                    'description': "Selon les d꤬arations du président colombien Juan Manuel Santos, le bilan de la gigantesque coulée de ",
                    'provider': [{'_type': 'Organization', 'name': 'Le Point'}],
                    'datePublished': '2017-04-03T10:33:00',
                    'headline': True,
                    'clusteredArticles': [{'name': "Colombie : le bilan s'alourdit de 54 orts, dont 43 enfants",
                                           'url': 'http://www.bing.com/cr?IG=CEFF9C63FD7A4439B591261606484860&CID=3B75F5FD9A146DBF103CFFA49BF36C83&rd=1&h=',
                                           'description': "La ville de Mocoa, capitale provinciale du sud du pays, a été frappée ces derniers ...",
                                           'provider': [{'_type': 'Organization', 'name': 'Le Figaro'}],
                                           'datePublished': '2017-04-03T09:38:00', 'headline': True},
        ...

    """
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'q': query,
        'count': "{0}".format(count),
        'offset': "{0}".format(offset),
        'mkt': market,
        'safeSearch': 'Moderate',
    })

    try:
        conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/news/search?%s" %
                     params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return bytes2python(data)
    except Exception as e:
        raise CognitiveException("[Errno {0}] {1}".format(e.errno, e.strerror))


def call_api_speech_reco(subkey, lang="fr-FR", filename=None, memwav=None,
                         url="https://speech.platform.bing.com/recognize"):
    """
    Implemented in module
    `ensae_teaching_cs <http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx3/py-modindex.html>`_.
    Only available on Windows for the time being (relies on C# code).

    @param      subkey      subscription key
    @param      lang        language
    @param      filename    wav file
    @param      memwav      wav memory stream
    @param      url         url of the service
    @return                 dictionary wih the results

    Either filename or memwav must be specified.
    """
    from ensae_teaching_cs.pythonnet import vocal_recognition
    return vocal_recognition(subkey, lang=lang, filename=filename, memwav=memwav, url=url)


def call_api_emotions(subkey, image_or_bytes):
    """
    Retrieve resuls for news

    @param      subkey              subscription key
    @param      image_or_bytes      image or bytes
    @return                         results
    """
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subkey,
    }

    params = urllib.parse.urlencode({
    })

    if isinstance(image_or_bytes, str):
        with open(image_or_bytes, "rb") as f:
            content = f.read()
    else:
        content = image_or_bytes

    try:
        conn = http.client.HTTPSConnection(
            'westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?%s" %
                     params, content, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return bytes2python(data)
    except Exception as e:
        raise CognitiveException("[Errno {0}] {1}".format(e.errno, e.strerror))
