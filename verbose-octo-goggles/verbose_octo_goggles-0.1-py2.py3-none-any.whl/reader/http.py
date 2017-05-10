from lxml import etree

import requests
from verbose_octo_goggles.core import SkipItem
from verbose_octo_goggles.reader.base import BaseReader


class XmlFromHttpReader(BaseReader):
    def process_unit(self, unit):
        res = requests.get(unit)
        if res.status_code == 200:
            return etree.fromstring(res.content)
        else:
            self.logger.error('Unit response with status {}, skipping'.format(res.status_code))
            raise SkipItem
