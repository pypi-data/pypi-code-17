import json

import requests
from pyquery import PyQuery as pq

from base import BaseCrawler


class DizistCrawler(BaseCrawler):
    def __init__(self):
        BaseCrawler.__init__(self)

    def generate_episode_page_url(self):
        return "http://www.dizist1.com/izle/" + self.episode['dizi_url'] + "-" + \
               str(self.episode['season']) + "-sezon-" + str(self.episode['episode']) + "-bolum"

    def after_body_loaded(self, text):
        page_dom = pq(text)
        player_address = page_dom("iframe[src^='http://www.dizist1.com']").attr('src')

        result = requests.get(player_address, headers=BaseCrawler.headers)

        if result.status_code == 200:
            self.after_sources_loaded(result.text)

    def after_sources_loaded(self, text):
        page_dom = pq(text)
        sourcesJson = page_dom(".dzst-player").attr("data-dzst-player")

        sources = json.loads(sourcesJson)
        sources = sources['tr']

        for source_key in sources.keys():
            video_link = {"res": str(source_key) + 'p', "url": sources[source_key]}
            self.episode['video_links'].append(video_link)


