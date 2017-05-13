import copy
import json

import re

import demjson
import requests

from base import BaseDiziCrawler
from pyquery import PyQuery as pq


class SezonlukDiziCrawler(BaseDiziCrawler):
    def __init__(self):
        BaseDiziCrawler.__init__(self)

    def generate_episode_page_url(self):
        return "http://sezonlukdizi.net/" + self.episode['dizi_url'] + "/" + \
               str(self.episode['season']) + "-sezon-" + str(self.episode['episode']) + "-bolum.html"

    def after_body_loaded(self, text):
        page_dom = pq(text)
        player_address = "http:" + page_dom("iframe[height='360']").eq(0).attr("src")

        result = requests.get(player_address, headers=BaseDiziCrawler.headers)

        if result.status_code == 200:
            self.after_sources_loaded(result.text)

        self.episode['site'] = 'sezonlukdizi'

    def after_sources_loaded(self, text):
        videopush = re.compile(r"video\.push\(([^(]*)\);")
        for m in re.finditer(videopush, text):
            match = m.group(1)

            source = json.loads(match)

            if 'p' not in str(source['label']):
                source['label'] = str(source['label']) + 'p'

            if 'http' not in source['file']:
                source['file'] = 'http:' + source['file']

            video_link = {"res": source['label'], "url": source['file']}
            self.episode['video_links'].append(video_link)

        subpush = re.compile(r"altyazi\.push\(([^(]*)\);")
        for m in re.finditer(subpush, text):
            match = m.group(1)

            source = demjson.decode(match)

            if source['label'][0] == 'T':
                source['label'] = 'tr'
            elif source['label'][0] == 'E':
                source['label'] = 'en'

            if 'http' not in source['file']:
                source['file'] = 'http:' + source['file']

            subtitle_link = {"lang": source['label'], "url": source['file'], "kind": "vtt"}
            self.episode['subtitle_links'].append(subtitle_link)

        video = re.compile(r"var video = ([^(]*)\}\];")
        for m in re.finditer(video, text):
            match = m.group(1) + "}]"

            sources = json.loads(match)
            for source in sources:
                if 'p' not in str(source['label']):
                    source['label'] = str(source['label']) + 'p'

                if 'http' not in source['file']:
                    source['file'] = 'http:' + source['file']

                video_link = {"res": source['label'], "url": source['file']}
                self.episode['video_links'].append(video_link)

        sub = re.compile(r"var altyazi = ([^(]*)\}\];")
        for m in re.finditer(sub, text):
            match = m.group(1) + "}]"

            sources = json.loads(match)
            for source in sources:
                if source['label'][0] == 'T':
                    source['label'] = 'tr'
                elif source['label'][0] == 'E':
                    source['label'] = 'en'

                if 'http' not in source['file']:
                    source['file'] = 'http:' + source['file']

                subtitle_link = {"lang": source['label'], "url": source['file'], "kind": "vtt"}
                self.episode['subtitle_links'].append(subtitle_link)


