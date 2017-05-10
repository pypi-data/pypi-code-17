#!/usr/bin/env python
#-*-coding:utf-8-*-

# author : "qiulimao"
# email  : "qiulimao@getqiu.com"

""" 
 清洗数据
""" 
#---------- code begins below -------


from models import from_session,to_session,WebContent,RawWebContent
from lxml.html import fromstring,tostring
import pyquery
from HTMLParser import HTMLParser
import re 

utf8 = lambda string:string.encode("utf-8") if isinstance(string,unicode) else string 
u = lambda string: string  if isinstance(string,unicode) else string.decode("utf-8")
md5 = lambda string:hashlib.md5(utf8(string)).hexdigest()

def clean():
    """
        从from当中读数据，
        写到to数据库当中
    """
    pages = from_session.query(RawWebContent).order_by(RawWebContent.id.asc()).offset(500).limit(500).all()

    for p in pages:
        try:
            py_dom = pyquery.PyQuery(p.html)
            
            py_dom('script').remove()
            py_dom('style').remove()

            pure_html = py_dom.outer_html()

            py_dom("#main_content").remove()
            content_dom = pyquery.PyQuery(p.content_html)
            content_dom("script").remove()
            content_dom("style").remove()
            new_page = WebContent(title=p.title,url=p.url,html=pure_html,content=content_dom.outer_html(),noise=py_dom.outer_html())
            to_session.add(new_page)
            to_session.commit()
        except Exception:
            print "one error...."
            


if __name__ == "__main__":
    clean()