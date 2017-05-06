import copy
import json

import requests

from base import BaseDiziCrawler
from pyquery import PyQuery as pq


class DizimekCrawler(BaseDiziCrawler):
    def __init__(self):
        BaseDiziCrawler.__init__(self)

    def generate_episode_page_url(self):
        return "http://188.166.65.249/diziapi/" + self.episode['dizi_url'] + "/season/" + \
               str(self.episode['season']) + "/episode/" + str(self.episode['episode'])

    def after_body_loaded(self, text):
        sources = json.loads(text)
        self.episode['video_links'] = sources['video_links']
        self.episode['subtitle_links'] = sources['subtitle_links']

        self.episode['site'] = 'dizimek'



