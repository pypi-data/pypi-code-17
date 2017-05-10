#!/usr/bin/env python
#-*-coding:utf-8-*- 
from lxml.html import fromstring,tostring
import requests
import re
import pyquery
from HTMLParser import HTMLParser
import numpy as np
import random
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

def statistic_from_url(source):
    """
        html文本当中提取正文
    """
    if re.match(r"(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?",source):
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
        response = requests.get(source,headers=headers)
        html_source = response.text.encode(response.encoding).decode(response.apparent_encoding,"ignore")
        #html_source = pyquery.PyQuery(response.text.encode(response.encoding).decode(response.apparent_encoding,"ignore"))
        # 现在可以计算了。
        return statistic_from_htmlstring(html_source)
    else:
        return ["NotAnValideUrl","NotAnValideUrl"]

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
    for node in intesting_node:
        
        #if len(node.getchildren()):
        #    continue;
        
        if node.text and len(node.text) > 0:
            text = re.sub("[\s,.。，？（）&]+","",node.text)
            length = len(text)
            if length > 0:
                statistics.append(length)

    return statistics
        
def  density_feature():
    """
        统计密度相关特性。
    """
    from models import WebContent,to_session

    webcontents = to_session.query(WebContent).limit(800).all()

    data_list = []
    for web in webcontents:
        try:
            data_list.extend(statistic_from_htmlstring(web.content))
        except TypeError:
            print "error accourred.but go on..."
    
    np_data_array = np.array(data_list)
    #print np_data_array.mean(),np_data_array.var(),len(np_data_array)
    
    
    #for b in bins:
    #    print "the data is",b
    fig = plt.figure(figsize=(8,6), dpi=72, facecolor="white")  
    axes = plt.subplot(211)
    axes2 = plt.subplot(212)
    n,bins,patches = axes.hist(np_data_array,bins=map(lambda x:x-0.5,range(1,100)),histtype='bar',facecolor='yellowgreen',alpha=0.75)
    possibilty = []
    for count_n in n:
        possibilty.append(count_n/len(np_data_array))

    print possibilty

    axes2.bar(left=np.arange(0,len(possibilty)),height=np.array(possibilty))

    #print possibilty
    
    #axes.set_xlabel(u'density')
    axes.set_ylabel(u'count')
    axes.set_title(u'density count histogram for noise')
    axes.axis([0,150,0,10000])
    axes2.axis([0,150,0,0.15])
    ymajorLocator   = MultipleLocator(1000) #将y轴主刻度标签设置为500的倍数  
    #ymajorFormatter = FormatStrFormatter('%1.1f') #设置y轴标签文本的格式  
    yminorLocator   = MultipleLocator(500) #将此y轴次刻度标签设置为100的倍数 

    xmajorLocator = MultipleLocator(10)
    xminorLocator = MultipleLocator(1)

    axes.yaxis.set_major_locator(ymajorLocator)
    axes.yaxis.set_minor_locator(yminorLocator)

    axes.xaxis.set_major_locator(xmajorLocator)
    axes.xaxis.set_minor_locator(xminorLocator)

    
    axes.xaxis.grid(True, which='major') #x坐标轴的网格使用主刻度
    axes.yaxis.grid(True, which='minor') #y坐标轴的网格使用次刻度

    axes2.set_xlabel(u'density')
    axes2.set_ylabel(u'possibilty')
    axes2.set_title(u'density possibilty histogram for noise')

    axes2.yaxis.set_major_locator(MultipleLocator(0.05))
    axes2.yaxis.set_minor_locator(MultipleLocator(0.01))

    #axes2.xaxis.grid(True, which='major') #x坐标轴的网格使用主刻度
    axes2.yaxis.grid(True, which='minor') #y坐标轴的网格使用次刻度

    axes.text(130,8000,"total tags:%s\n average density:%f"%(len(np_data_array),round(np_data_array.mean(),4))\
             ,fontsize=15,verticalalignment="top",horizontalalignment="right")
    plt.show()


if __name__ == "__main__":
    density_feature()