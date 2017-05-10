#!/usr/bin/env python
#-*-coding:utf-8-*-

# author : "qiulimao"
# email  : "qiulimao@getqiu.com"
from lxml.html import fromstring,tostring
import requests
import re
import pyquery
from HTMLParser import HTMLParser
import numpy as np
import random
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
""" 
 label作用统计
""" 
#---------- code begins below -------

def statistic_from_htmlstring(source):
    """
    """
    html_source = pyquery.PyQuery(source)
    html_source("style").remove()
    html_source("script").remove()
    html_dom = fromstring(html_source.html())

    #intesting_node = html_dom.xpath("//p | //a | //span | //ul | //li | //font | //strong | //pre")
    sum_of_all_label = map(lambda s:len(html_dom.xpath(s)),["//p","//a","//span","//ul","//li","//font","strong","//pre"])

    return sum_of_all_label

def sumofallpage():
    """
    """
    from models import WebContent,to_session
    webcontents = to_session.query(WebContent).limit(800).all()
    result = [0,0,0,0,0,0,0,0]
    for w in webcontents:
        try:
            tmp = statistic_from_htmlstring(w.noise)
            result = map(lambda i:result[i]+tmp[i],range(0,len(result)))
        except TypeError:
            print "error accours,but goes on ...."

    
    return result

if __name__ == "__main__":
    result =  sumofallpage()
    countall = reduce(lambda x,y:x+y,result)
    possibilty = map(lambda x:float(x)/countall,result)
    print result
    print countall
    print possibilty