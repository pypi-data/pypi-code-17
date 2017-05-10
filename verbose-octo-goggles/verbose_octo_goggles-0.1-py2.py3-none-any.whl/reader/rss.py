from lxml import etree

import requests
from verbose_octo_goggles.core import SkipItem

from .base import BaseReader


class BaseRssReader(BaseReader):
    items_xpath = ''

    def __init__(self, *args, **kwargs):
        super(BaseRssReader, self).__init__(*args, **kwargs)
        self.root = None

    def data_stream(self):
        for source in self.get_sources():
            for item in self.extract_items_from_xml(source):
                yield source, item

    def process_url(self, url):
        res = requests.get(url)
        if res.status_code == 200:
            return etree.fromstring(res.content)
        else:
            raise SkipItem

    def extract_items_from_xml(self, etree_root):
        return etree_root.xpath(self.items_xpath)

    def get_sources(self):
        raise NotImplementedError
