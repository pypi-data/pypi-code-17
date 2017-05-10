#!/usr/bin/env python
#-*-coding:utf-8-*-

# author : "qiulimao"
# email  : "qiulimao@getqiu.com"

""" 
 统计标签的相似度
""" 
#---------- code begins below -------
from lxml.html import fromstring,tostring
import requests
import re
import pyquery
from HTMLParser import HTMLParser
import numpy as np
import random
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

def statistic_from_htmlstring(source):
    """
    """
    html_source = pyquery.PyQuery(source)
    html_source("style").remove()
    html_source("script").remove()
    html_dom = fromstring(html_source.html())

    intesting_node = html_dom.xpath("//p | //a | //span | //ul | //li | //font | //strong | //pre")
    statistics = []
    #print "%s element qualify" % len(intesting_node)
    similarity_data = []
    for node in intesting_node:
        
        # 跳过非叶子节点
        #if len(node.getchildren()):
        #    continue;

        tag = node.tag
        node_parent = node.getparent()
        similaritys = len(node_parent.xpath("./%s" % tag))
        similarity_data.append(similaritys)

    return similarity_data


def similarity_feature():
    """
        相似度分析
    """
    from models import WebContent,to_session
    webcontents = to_session.query(WebContent).limit(800).all()

    similarity_array = []
    for page in webcontents:
        try:
            similarity = statistic_from_htmlstring(page.noise)
            similarity_array.extend(similarity)
        except Exception as e:
            print e

    
    np_similarity_array = np.array(similarity_array)
    plt1 = plt.subplot(211)
    plt2 = plt.subplot(212)
    n,bins,pathces = plt1.hist(np_similarity_array,bins=map(lambda x:x-0.5,range(1,100)),histtype='bar',facecolor='yellowgreen',alpha=0.75)
    size = len(similarity_array)

    np_similarity_possibility = map(lambda x:float(x)/size,n)
    print np_similarity_possibility
    plt2.bar(left=np.arange(0,len(n)),height=np_similarity_possibility,facecolor='red',alpha=0.75)

    #plt1.set_xlabel(u'similarity')
    plt1.set_ylabel(u'count')
    plt1.set_title(u'similarity count histogram for content')
    plt1.text(80,10000,"total tags:%d" % (size)\
             ,fontsize=15,verticalalignment="top",horizontalalignment="right")
    plt2.set_xlabel(u'similarity')
    plt2.set_ylabel(u'possibilty')
    plt2.set_title(u'similarity possibilty histogram for content')   
    plt.show()

if __name__ == "__main__":
    similarity_feature()

            