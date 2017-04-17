
#encoding:utf-8

import requests, re, json
from bs4 import BeautifulSoup


#
headers = {'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}



# 搜索盘搜
def search_pansou(query_key):

    url = 'http://api.pansou.com/search_new.php?q=%s' % query_key
    j = requests.get(url=url, headers=headers).json()
    if j['listcount'] > 0:
        items = j['list']['data']
        if items:
            return [item['link'] for item in items if item['host'] == 'pan.baidu.com']
        else:
            return None
    else:
        return None



# 搜索户户盘
def search_huhupan(query_key):
    search_url = 'http://huhupan.com/e/search/index.php'
    data = {
        'keyboard': query_key,
        'show': 'title',
        'tempid': 1,
        'tbname': 'news',
        'mid': 1,
        'dopost': 'search'
    }
    r = BeautifulSoup(requests.post(url=search_url,headers=headers,data=data).content, 'html.parser')
    # find_all( name , attrs , recursive , text , **kwargs ) - 搜索当前tag的所有tag子节点,并判断是否符合过滤器的条件
    items_list = r.find_all('span', {'class': 'more'})
    yunpan_href = []

    if items_list:
        for item in items_list:
            # find( name , attrs , recursive , text , **kwargs )
            # 它与 find_all() 方法唯一的区别是 find_all() 方法的返回结果是值包含一个元素的列表,而 find() 方法直接返回结果
            # 取出a标签中的href内容 如： http://huhupan.com/zyjm/2017-01-08/10180.html

            # temp_href 获取的链接和密码
            temp_href = huhupan_url(item.find('a')['href'])
            if temp_href:
                # extend() 函数用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
                yunpan_href.extend(temp_href)

    else:
        return None
    return yunpan_href


def huhupan_url(url):
    r = BeautifulSoup(requests.get(url=url, headers=headers).content, 'html.parser')
    # 过滤，寻找标签a中，带有class':'meihua_btn 和 href 的
    baiduyun_href = r.find('a',{'class':'meihua_btn','href':re.compile(r'/e/extend/down/.*')})

    if baiduyun_href:
        # 拼接字符串 - baiduyun_href['href'(baiduyun_href中的href内容) 如： http://huhupan.com/e/extend/down/?id=10774
        baiduyun_url = 'http://huhupan.com' + baiduyun_href['href']
        # 获取链接和密码
        yunpan_href = parse_huhupan(baiduyun_url)
        if yunpan_href:
            return yunpan_href
        else:
            return None
    else:
        return None

def parse_huhupan(url):
    r = BeautifulSoup(requests.get(url=url, headers=headers).content, 'html.parser')
    # 过滤，寻找标签a中，带有class':'meihua_btn 和 href 的
    # 如 <a class="meihua_btn" href="http://pan.baidu.com/s/1o8dfINS">170108-0129-P61</a>
    href_list = r.find_all('a', {'class': 'meihua_btn', 'href': re.compile(r'http://pan\.baidu\.com/.*')})
    # 提取密码 寻找含有input标签 id=foo*  <input id="foo1" value="6q0z" size="4">
    pwd_list = r.find_all('input', {'id': re.compile(r'foo[0-9]')})
    if pwd_list:
        #print('~~~~~~~~~~~~~~~~~~')
        # 位置方法格式化  >>> '{}.{}'.format('pythontab', 'com') -> 'pythontab.com'
        #print(['链接:{},密码:{}'.format(href_list[x]['href'], pwd_list[x]['value']) for x in range(len(href_list))])
        return ['链接:{},密码:{}'.format(href_list[x]['href'], pwd_list[x]['value']) for x in range(len(href_list))]
    else:
        return None



# 搜索去转盘
def search_quzhuanpan(query_key):

    def parse_quzhuanpan(url):

        pass

    def quzhuanpan_url(url):
        r1 = BeautifulSoup(requests.get(url=url, headers=headers).content, 'html.parser')
        # baiduyun_href -> 字符串
        baiduyun_href = r1.find('a', {'href': re.compile(r'https://pan\.baidu\.com/.*')})['href']
        # 下面两行代码是转成list
        p = re.compile(r'https://pan\.baidu\.com/.*')
        return p.findall(baiduyun_href)

        # if baiduyun_href:
        #     baiduyun_url = baiduyun_href['href']
        #     yunpan_href = parse_quzhuanpan(baiduyun_url)
        #     if yunpan_href:
        #         return yunpan_href
        #     else:
        #         return None
        # else:
        #     return None


    url = 'http://www.quzhuanpan.com/source/search.action?q=%s' % query_key
    r = BeautifulSoup(requests.get(url=url, headers=headers).content, 'html.parser')
    items_list = r.find_all('h4', {'class': 'result4 next-row'})

    quzhuanpan_href = []
    if items_list:
        for item in items_list:
            temp_href = quzhuanpan_url(('http://www.quzhuanpan.com' + item.find('a')['href']))
            if temp_href:
                quzhuanpan_href.extend(temp_href)

    else:
        return None
    return quzhuanpan_href









# 搜索电影
def search_movice(keyword):
    query_key = keyword
    l = []
    try:
        huhupan_result = search_huhupan(query_key)
        if huhupan_result:
            print('1')
            l.extend(huhupan_result)
    except:
        pass

    try:
        pansou_result = search_pansou(query_key)
        if pansou_result:
            print('2')
            l.extend(pansou_result)
    except:
        pass


    try:
        quzhuanpan_result = search_quzhuanpan(query_key)
        if quzhuanpan_result:
            print('3')
            l.extend(quzhuanpan_result)
    except:
        pass

    #print('L=', l)
    return l

# if __name__=='__main__':
#    #search_quzhuanpan('生化危机5')
#    search_movice('生化危机')




