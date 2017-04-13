"""
Tools for getting and opening YTMND pages
"""

import html
import re
import urllib.request


ERROR_TOP_SITES = """[!] Couldn't get the top-sites page!  Maybe your internet is down?
PUNCH THE KEYS, FOR GOD'S SAKE!"""
YTMND_TOP_SITE_URL = "http://ytmnd.com/sites/top_rated/alltime"
YTMND_SITE_REGEX = rb'''"site_link" href="([^"]+)" title="([^"]+)"  rel="external">'''


def decode_site_info(site):
    (url, title) = site    
    url = url.decode('utf-8')
    title = html.unescape(title.decode('utf-8'))
    return (url, title)


def get_top_site_html():
    try:
        return urllib.request.urlopen(YTMND_TOP_SITE_URL).read()
    except:
        exit(ERROR_TOP_SITES)


def fetch_top_sites():
    html = get_top_site_html()
    encoded_sites = re.findall(YTMND_SITE_REGEX, html)
    sites = list(map(decode_site_info, encoded_sites))
    return sites
