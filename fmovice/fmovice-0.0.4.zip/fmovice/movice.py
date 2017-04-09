#encoding:utf-8
import requests,re,json
from bs4 import BeautifulSoup

headers = {'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

def search_pansou(query_key):

    url = 'http://api.pansou.com/search_new.php?q=%s'%query_key.decode('utf-8')
    
    j = requests.get(url=url,headers=headers).json()

    if j['listcount'] > 0:
        items = j['list']['data']
        if items:
            return [item['link'] for item in items if item['host'] == 'pan.baidu.com']
        else:
            return None
    else:
        return None

def search_huhupan(query_key):

    search_url = 'http://huhupan.com/e/search/index.php'
    data = {
        'keyboard':query_key,
        'show':'title',
        'tempid':1,
        'tbname':'news',
        'mid':1,
        'dopost':'search'
    }
    r = BeautifulSoup(requests.post(url=search_url,headers=headers,data=data).content,'lxml')
    items_list = r.find_all('span',{'class':'more'})

    yunpan_href = []

    if items_list:
        for item in set(items_list):
            temp_href = huhupan_url(item.find('a')['href'])
            if temp_href:
                yunpan_href.extend(temp_href)
    else:
        return None

    return yunpan_href

def huhupan_url(url):
    r = BeautifulSoup(requests.get(url=url,headers=headers).content,'lxml')
    baiduyun_href = r.find('a',{'class':'meihua_btn','href':re.compile(r'/e/extend/down/.*')})

    if baiduyun_href:
        baiduyun_url = 'http://huhupan.com' + baiduyun_href['href']
        yunpan_href = parse_huhupan(baiduyun_url)
        
        if yunpan_href:
            return yunpan_href
        else:
            return None
    else:
        return None


def parse_huhupan(url):
    r = BeautifulSoup(requests.get(url=url,headers=headers).content,'lxml')
    href_list = r.find_all('a',{'class':'meihua_btn','href':re.compile(r'http://pan\.baidu\.com/.*')})
    pwd_list = r.find_all('input',{'id':re.compile(r'foo[0-9]')})
    

    if pwd_list:
        return ['链接:{},密码:{}'.format(href_list[x]['href'],pwd_list[x]['value']) for x in range(len(href_list))]
    else:
        return None

def search_movice(keyword):
    query_key = keyword
    l = []

    try:
        huhupan_result = search_huhupan(query_key)
        if huhupan_result:
            l.extend(huhupan_result)
    except:
        pass

    try:
        pansou_result = search_pansou(query_key)
        if pansou_result:
            l.extend(pansou_result)
    except:
        pass

    return l