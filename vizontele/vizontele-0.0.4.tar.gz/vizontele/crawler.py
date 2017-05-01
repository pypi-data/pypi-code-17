import vizontele
from diziay import DiziayCrawler
from dizibox import DiziboxCrawler
from dizilab import DizilabCrawler
from dizipub import DizipubCrawler
from dizist import DizistCrawler
from sezonlukdizi import SezonlukDiziCrawler
from dizimag import DizimagCrawler
from dizimek import DizimekCrawler

dizisites = {
    "dizilab": DizilabCrawler,
    "dizipub": DizipubCrawler,
    "sezonlukdizi": SezonlukDiziCrawler,
    "dizimag": DizimagCrawler,
    "dizibox": DiziboxCrawler,
    "diziay": DiziayCrawler,
    "dizist": DizistCrawler,
    "dizimek": DizimekCrawler,
}


class Crawler:
    def __init__(self, site, dizi_url, season_number, episode_number):
        self.site = site
        if self.site in dizisites.keys():
            self.dizicrawler = dizisites[self.site]()
        elif self.site == '':
            self.dizicrawler = None

        self.episode = {"dizi_url": vizontele.slugify(dizi_url),
                        "season": season_number,
                        "episode": episode_number}

    def get_sources(self):
        """
        Runs the crawler and returns the episode with found video and subtitle links
        :return: episode dict
        """
        if self.dizicrawler is not None:
            self.episode = self.dizicrawler.get_sources(self.episode)
        else:
            # Site is not specified, lets check them all
            for site in dizisites.keys():
                self.dizicrawler = dizisites[site]()
                self.episode = self.dizicrawler.get_sources(self.episode)
                if 'video_links' in self.dizicrawler.episode and len(self.dizicrawler.episode['video_links']) > 0:
                    break

        return self.episode

