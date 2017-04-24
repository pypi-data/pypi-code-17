import copy
import json

import re
import requests

from base import BaseCrawler
from pyquery import PyQuery as pq


class DiziayCrawler(BaseCrawler):
    def __init__(self):
        BaseCrawler.__init__(self)

    def generate_episode_page_url(self):
        return "http://diziay.com/izle/" + self.episode['dizi_url'] + "-" + \
               str(self.episode['season']) + "-sezon-" + str(self.episode['episode']) + "-bolum/"

    def after_body_loaded(self, text):
        page_dom = pq(text)
        player_address = page_dom("iframe[height='375']").attr("src")
        ajax_address = player_address.replace("dizi-oynat", "ajax")

        ajax_headers = copy.copy(BaseCrawler.headers)
        ajax_headers['X-Requested-With'] = 'XMLHttpRequest'
        result = requests.get(ajax_address, headers=ajax_headers)

        if result.status_code == 200:
            self.after_sources_loaded(result.text)

    def after_sources_loaded(self, text):
        sources = json.loads(text)['success']

        for source in sources:
            video_link = {"res": source['label'], "url": source['src']}
            if "mp4" in source['type']:
                self.episode['video_links'].append(video_link)


