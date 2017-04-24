import vizontele
from diziay import DiziayCrawler
from dizibox import DiziboxCrawler
from dizilab import DizilabCrawler
from dizipub import DizipubCrawler
from dizist import DizistCrawler
from sezonlukdizi import SezonlukDiziCrawler

dizisites = {
    "dizilab": DizilabCrawler,
    "dizipub": DizipubCrawler,
    "sezonlukdizi": SezonlukDiziCrawler,
    "dizimek": SezonlukDiziCrawler,
    "dizimag": SezonlukDiziCrawler,
    "dizibox": DiziboxCrawler,
    "diziay": DiziayCrawler,
    "dizist": DizistCrawler,
    "onlinedizi": SezonlukDiziCrawler,
    "dizinow": SezonlukDiziCrawler
}


class Crawler:
    def __init__(self, site, callback, dizi_url, season, episode):
        self.site = site
        self.callback = callback
        self.crawler = dizisites[self.site]()
        self.episode = {"dizi_url": vizontele.slugify(dizi_url), "season": season, "episode": episode}

    def run(self):
        self.crawler.get_sources(self.episode, self.callback)
