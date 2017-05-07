# botf/dutch/spider.py
#
#

""" Spider plugin. """

## IMPORTS

from .url import parse_urls, parse_url, need_redirect, get_url
from .trace import get_exception
from .space import kernel
from .object import Object
from .utils import now

import logging
import time

url_list = []

class Spider(Object):

    pass

class SpiderData(Object):

    pass

class SpiderServer(Object):

    def __init__(self, *args, **kwargs):
        Object.__init__(self, *args, **kwargs)
        self.errors = []
        self.urls = []
        self.url = Object()
        self.followed = []
        self.speed = 0.1
        self.depth = 10 

    def crawl(self, *args, **kwargs):
        from .space import kernel
        for obj in kernel.find("spider"):
            logging.warn("spider %s" % obj.spider)
            self.crawl_url(obj.spider)

    def crawl_url(self, *args, **kwargs):
        #time.sleep(self.depth * self.speed)
        try:
            url, search = args
        except ValueError:
            url = args[0]
            search = ""
        logging.warn("# crawl %s" % url)
        urls = []
        urldata = Object()
        urldata.url = url
        urldata.basepath, urldata.base, urldata.root, urldata.file = parse_url(urldata.url)
        pnr = len(url.split("/"))
        if pnr >  self.depth:
            logging.warn("%s max depth " % url)
            return
        if url not in self.urls and url not in url_list: 
            self.urls.append(url)
            try:
                resp = get_url(url)
            except:
                logging.error(get_exception())
                return
            o = SpiderData()
            newurl = need_redirect(resp)
            if newurl:
                logging.warn("redirecting to %s" % newurl)
                resp = get_url(newurl).data
            newurl2 = need_redirect(resp)
            if newurl2:
                logging.warn("redirecting to %s" % newurl2)
                resp = get_url(newurl2).data
            if search:
                div = extract_div(search, resp.data)
                if div:
                    o.txt = strip_html(div)
                    o.save()
            else:
                o.content = str(resp.data, "utf-8")
                o.save()
            urls = parse_urls(url, resp.data)
            for u in urls:
                if u in self.urls:
                    continue
                if not urldata.base in u:
                    continue
                if u in self.errors:
                   continue
                self.urls.append(u)
                self.crawl_url(u, search)
        self.sync()
        return urls

## INIT

def spider(event):
    s = Spider()
    s.spider = event._parsed.args[0]
    s.save()
    event.ok(1)

def crawl(event):
    s = SpiderServer()
    s.crawl()
    for url in s.urls:
        event.reply(url)

## INIT

def init(*args, **kwargs):
    spider = SpiderServer()
    spider.crawl()
    return spider
