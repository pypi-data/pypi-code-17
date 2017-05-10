#!/usr/bin/env python
#-*-coding:utf-8-*-

# author : "qiulimao"
# email  : "qiulimao@getqiu.com"

""" 
 bayes
""" 
#---------- code begins below -------
from math import log10
from lxml.html import fromstring,tostring
import requests
import re
import pyquery
from HTMLParser import HTMLParser

P_content = 0.1
P_noise = 0.9

P_tagp_Y = 0.596
P_tagp_N = 0.167

P_taga_Y = 0.176
P_taga_N = 0.416

P_tagspan_Y = 0.081
P_tagspan_N = 0.074

P_tagul_Y = 0.000001
P_tagul_N = 0.064

P_tagli_Y = 0.000001
P_tagli_N = 0.278

P_tagfont_Y = 0.0146
P_tagfont_N = 0.000001

P_tagstrong_Y = 0.000001
P_tagstrong_N = 0.000001

P_tagpre_Y = 0.000001
P_tagpre_N = 0.000001

P_tag_map_Y = {"p":0.596,"a":0.176,"span":0.081,"ul":0.000001,"li":0.000001,"font":0.0146,"strong":0.000001,"pre":0.000001}
P_tag_map_N = {"p":0.167,"a":0.416,"span":0.074,"ul":0.064,"li":0.278,"font":0.000001,"strong":0.000001,"pre":0.000001}

P_density_Y = [0.02628388535958489, 0.13825711653169098, 0.05106444886280976, 0.042286988991804469, 
    0.010135298967072402, 0.014742253043014403, 0.011347655302846612, 0.011493138063139518, 
    0.0096503564327627168, 0.011008195528829834, 0.011444643809708549, 0.011056689782260803, 
    0.010038310460210465, 0.0093108966587459388, 0.0083410115901265697, 0.008098540322971727, 
    0.0069346782406284856, 0.0069831724940594541, 0.006449735706318801, 0.0067407012269046114, 
    0.0053828621308374958, 0.0055768391445613691, 0.0047524368362349065, 0.0048979195965278112, 
    0.0049464138499587798, 0.0051888851171136216, 0.0048494253430968427, 0.004800931089665875, 
    0.0036855632607536008, 0.0043159885553561905, 0.003928034527908443, 0.0039765287813394116, 
    0.0053343678774065272, 0.0032976092333058533, 0.0042190000484942534, 0.0041220115416323163, 
    0.0040250230347703801, 0.003928034527908443, 0.0045099655690800638, 0.0032006207264439162, 
    0.0036855632607536008, 0.003831046021046506, 0.0036370690073226322, 0.003831046021046506, 
    0.0035400805004606956, 0.003831046021046506, 0.0035400805004606956, 0.0044614713156490952, 
    0.0047039425828039379, 0.0040735172882013478, 0.0040250230347703801, 0.0042190000484942534, 
    0.0049949081033897483, 0.0044129770622181276, 0.0029096552058581059, 0.0040735172882013478, 
    0.004364482808787159, 0.0037340575141845693, 0.003928034527908443, 0.004800931089665875, 
    0.0051888851171136216, 0.0041705057950632849, 0.0036855632607536008, 0.0041705057950632849, 
    0.0042190000484942534, 0.0045584598225110323, 0.0049464138499587798, 0.0052858736239755587, 
    0.0040250230347703801, 0.003928034527908443, 0.0048494253430968427, 0.004800931089665875, 
    0.0044614713156490952, 0.0050434023568207169, 0.0045584598225110323, 0.0049949081033897483, 
    0.0044614713156490952, 0.0037340575141845693, 0.0047524368362349065, 0.0035885747538916637, 
    0.004267494301925222, 0.0043159885553561905, 0.0034915862470297271, 0.0044614713156490952, 
    0.003831046021046506, 0.0037825517676155374, 0.0037340575141845693, 0.0044129770622181276, 
    0.0036855632607536008, 0.0046069540759420009, 0.0031521264730129481, 0.0041220115416323163, 
    0.0036370690073226322, 0.0041705057950632849, 0.0046554483293729694, 0.0041705057950632849, 
    0.003928034527908443, 0.0035400805004606956]

_P_density_N = [0.031179825831136009, 0.10038573787038269, 0.039371865390784543, 0.0387537458824634, 
    0.026759097702003801, 0.0084111198917117217, 0.03741579099736321, 0.044074268232569422, 
    0.031179825831136009, 0.0063063838443903697, 0.074839406292300112, 0.024216200990556071, 
    0.012957036782022894, 0.024145782312392904, 0.069041601790199289, 0.049817302651654446, 
    0.037306250831331614, 0.074847230589873789, 0.062210990008371998, 0.037368845211921096, 
    0.037361020914347412, 0.037407966699789526, 0.049887721329817614, 0.031132880045693898, 
    0.0, 0.006243789463800887, 0.0, 7.8242975736853227e-06, 0.0, 0.0, 0.0, 0.0, 1.5648595147370645e-05, 0.0, 
    1.5648595147370645e-05, 0.0, 0.0, 0.0, 7.8242975736853227e-06, 7.8242975736853227e-06, 
    0.0, 0.0, 0.0, 7.8242975736853227e-06, 7.8242975736853227e-06, 0.0, 0.0, 7.8242975736853227e-06, 
    1.5648595147370645e-05, 7.8242975736853227e-06, 1.5648595147370645e-05, 7.8242975736853227e-06, 
    1.5648595147370645e-05, 2.3472892721055968e-05, 0.0, 0.0, 0.0, 1.5648595147370645e-05, 
    2.3472892721055968e-05, 3.1297190294741291e-05, 7.8242975736853227e-06, 1.5648595147370645e-05, 
    7.8242975736853227e-06, 1.5648595147370645e-05, 7.8242975736853227e-06, 7.8242975736853227e-06, 
    0.0, 7.8242975736853227e-06, 2.3472892721055968e-05, 2.3472892721055968e-05, 3.1297190294741291e-05, 
    1.5648595147370645e-05, 3.1297190294741291e-05, 7.8242975736853227e-06, 2.3472892721055968e-05, 
    2.3472892721055968e-05, 7.8242975736853227e-06, 7.8242975736853227e-06, 3.9121487868426613e-05, 
    7.8242975736853227e-06, 0.0, 1.5648595147370645e-05, 0.0, 1.5648595147370645e-05, 
    7.8242975736853227e-06, 0.0, 3.1297190294741291e-05, 1.5648595147370645e-05, 2.3472892721055968e-05, 
    2.3472892721055968e-05, 7.8242975736853227e-06, 2.3472892721055968e-05, 0.0, 1.5648595147370645e-05, 
    2.3472892721055968e-05, 7.8242975736853227e-06, 3.1297190294741291e-05, 7.8242975736853227e-06]


_P_similarity_Y = [0.365564738292011, 0.04634986225895317, 0.02572314049586777, 0.014600550964187328, 
    0.014118457300275482, 0.008264462809917356, 0.009400826446280992, 0.008815426997245178, 0.009607438016528925, 
    0.008953168044077135, 0.006060606060606061, 0.010743801652892562, 0.012982093663911846, 0.01012396694214876, 
    0.00878099173553719, 0.009366391184573003, 0.010537190082644627, 0.015495867768595042, 0.017665289256198348, 
    0.01584022038567493, 0.02097107438016529, 0.012121212121212121, 0.011880165289256199, 0.011570247933884297, 
    0.012052341597796144, 0.011639118457300276, 0.017665289256198348, 0.00674931129476584, 0.010984848484848484, 
    0.011363636363636364, 0.005337465564738292, 0.007713498622589532, 0.00909090909090909, 0.0035123966942148762, 
    0.0084366391184573, 0.006198347107438017, 0.006370523415977962, 0.003925619834710744, 0.009400826446280992, 
    0.006887052341597796, 0.004235537190082644, 0.007231404958677686, 0.004442148760330579, 0.006060606060606061, 
    0.0046487603305785125, 0.007920110192837466, 0.003236914600550964, 0.006611570247933884, 0.00674931129476584, 
    0.0, 0.0, 0.001790633608815427, 0.0, 0.005578512396694215, 0.001893939393939394, 0.003856749311294766, 0.0, 
    0.003994490358126722, 0.008126721763085399, 0.004132231404958678, 0.0021005509641873277, 0.0, 0.0, 0.0, 
    0.002238292011019284, 0.0022727272727272726, 0.0, 0.0, 0.0, 0.0024104683195592287, 0.007334710743801653, 
    0.0024793388429752068, 0.0025137741046831956, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0028236914600550966, 
    0.0028581267217630854, 0.0, 0.0, 0.0059228650137741045, 0.0, 0.0, 0.003064738292011019, 0.0, 0.006267217630853994, 
    0.0, 0.0, 0.0, 0.0, 0.003305785123966942, 0.0, 0.0]

_P_similarity_N = [0.5354691605269443, 0.09957557829753615, 0.043357157293255184, 0.08317930438936558, 
    0.01477208003380675, 0.034989986587539275, 0.08200341742150036, 0.046653315450052364, 0.0, 
    0.0, 0.0, 0.0, 0.002323, 0.00123, 0.00098, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
    0.0, 0.0]
set_zero_to_nozero = lambda x:x if x > 0.0 else 1e-4    

P_density_N = map(set_zero_to_nozero,_P_density_N)
P_similarity_Y = map(set_zero_to_nozero,_P_similarity_Y)
P_similarity_N = map(set_zero_to_nozero,_P_similarity_N)

def extract_from_url(source,text_only=False):
    """
        html文本当中提取正文
    """
    if re.match(r"(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?",source):
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
        response = requests.get(source,headers=headers)
        #html_source = pyquery.PyQuery(response.text.encode(response.encoding).decode(response.apparent_encoding,"ignore"))

        html_source = response.text.encode(response.encoding).decode(response.apparent_encoding,"ignore")
        #html_source = pyquery.PyQuery(response.content)
        return extract_from_htmlstring(html_source,text_only)
    else:
        return ["NotAnValideUrl","NotAnValideUrl"]
        
def extract_from_htmlstring(source,text_only=False):
    """

    """
    html_source = pyquery.PyQuery(source)
    html_source("style").remove()
    html_source("script").remove()
    html_source("*").removeAttr("class")
    html_source("*").removeAttr("style")
    lxml_dom = fromstring(html_source.html())
    
    html_tags = lxml_dom.xpath("//p | //a | //span | //ul | //li | //font | //strong | //pre")

    for tag in html_tags:
        """
            need to get three vector
            tag,
            density,
            similarity
        """
        tag_name = tag.tag # tag function
        tag_parent = tag.getparent()
        similarity = len(tag_parent.xpath("./%s" % tag_name)) # similarity
        similarity = similarity if similarity < len(P_similarity_N) else 60
        charactors = tag.text_content()
        text_content = charactors if charactors else " "
        text = re.sub("[\s,.。，？（）&]+","",text_content)
        density = len(text) # density
        density = density if density < len(P_density_Y) else 60

        ##
        #
        ##
        pYes = log10(P_content*P_tag_map_Y.get(tag_name,0.00001)*P_density_Y[density]*P_similarity_Y[similarity])
        pNo = log10(P_noise*P_tag_map_N.get(tag_name,0.000001)*P_density_N[density] * P_similarity_N[similarity])
        
        # is the tag be procced
        tag.proccesed = True
        tag.similarity = similarity
        tag.density = density

        tag.is_content = True if pYes > pNo else False


    ##
    # get all the content
    ##
    possible_main_body = lxml_dom.xpath("//div")

    if not possible_main_body:
        """
            the html doc does not have div section
        """
        return [None,None]
    
    THE_CONTENT = None 
    THE_CONTENT_RATIO = 0

    for div in possible_main_body:
        """
            calculate the possible body
        """
        [p,n] = calculate_non_leaf_node_info(div)
        #ratio = float(p) / (-10/(4*n+1) +20)
        ratio = p - n
        # ratio = 0.0
        # if n <= 0:
        #    ratio = float(p) / (n + 1)
        # else:
        #    ratio = float(p) / n

        #print "(p=%d,n=%d) %s ratio is %f" % (p,n,div,ratio)
        if(ratio > THE_CONTENT_RATIO):
            THE_CONTENT_RATIO = ratio
            THE_CONTENT = div

    if not text_only:
        content = re.sub(r"\s{1,}"," ",tostring(THE_CONTENT))
        parser = HTMLParser()
        return parser.unescape(content)
    else:
        content = re.sub(r"\s{1,}"," ",THE_CONTENT.text_content())
        return content



def is_the_tag_belongs_to_content(node):
    """
        is the specific tag belong to content
    """
    tag = node
    tag_name = tag.tag # tag function
    tag_parent = tag.getparent()
    similarity = len(tag_parent.xpath("./%s" % tag_name)) # similarity
    similarity = similarity if similarity < len(P_similarity_N) else 60
    text_content = tag.text if tag.text else " "
    text = re.sub("[\s,.。，？（）&]+","",text_content)
    density = len(text) # density
    density = density if density < len(P_density_Y) else 60

    ##
    #
    ##
    pYes = log10(P_content*P_tag_map_Y.get(tag_name,0.00001)*P_density_Y[density]*P_similarity_Y[similarity])
    pNo = log10(P_noise*P_tag_map_N.get(tag_name,0.000001)*P_density_N[density] * P_similarity_N[similarity])
    
    # is the tag be procced
    tag.proccesed = True
    tag.similarity = similarity
    tag.density = density

    tag.is_content = True if pYes > pNo else False 

    return [pYes >= pNo,tag_name,similarity,density]


def test_sample():
    from models import to_session,WebContent
    webcontents = to_session.query(WebContent).limit(800).all()

    all_label_count = 0
    content_count = 0
    for web in webcontents:
        try:
            html_dom = fromstring(web.content)
            for html_label in html_dom.xpath("//p | //a | //span | //ul | //li | //font | //strong | //pre"):
                all_label_count += 1 
                result = is_the_tag_belongs_to_content(html_label)
                if result[0]:
                    content_count += 1
        except TypeError:
            print "error accourred.but go on..."
    print all_label_count,content_count,float(content_count)/all_label_count

def calculate_non_leaf_node_info(node):
    """
        计算每个非叶子节点的信息含量
    """
    if hasattr(node,"proccesed"):
        if getattr(node,"is_content"):
            #positive = getattr(node,"similarity")*getattr(node,"density")
            positive = getattr(node,"density")
            return [positive,0]
        else:
            #negetive = getattr(node,"similarity")*getattr(node,"density")
            negetive = getattr(node,"density")
            return [0,negetive]

    positive_sum = 0
    negtive_sum = 0

    child_nodes = node.getchildren()

    for child_node in child_nodes:
        p = 0
        n = 0
        # 这里节省开销，如果算过了信号和噪声总量，那么缓存起来，下一轮就不再计算了
        if child_node.tag=='div':
            if hasattr(child_node,"IE") and hasattr(child_node,"NE"):
                p = getattr(child_node,"IE")
                n = getattr(child_node,"NE")
            else:
                p,n= calculate_non_leaf_node_info(child_node)
                setattr(child_node,"IE",p)
                setattr(child_node,'NE',n)
        else:
            p,n= calculate_non_leaf_node_info(child_node)

        positive_sum += p
        negtive_sum += n
    return [positive_sum,negtive_sum]


if __name__ == "__main__":
    url = "http://money.163.com/17/0315/05/CFI19QVG002580S6.html"
    test_sample()