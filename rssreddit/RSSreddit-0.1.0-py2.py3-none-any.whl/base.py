from .util import getXML, recurseXML

class BaseRSS(object):
    # URL = "http://www.reddit.com"
    def __init__(self, rss):
        self.URL = rss

    def make_request(self, category, sort="hot"):
        self.xml = getXML(self.URL+category+"/.rss")
        if self.xml:
            return recurseXML(self.xml)

    def comments(self, ID = ""):
        return self.make_request("comments")

    def gilded(self, arg):
        return self.make_request("gilded")
