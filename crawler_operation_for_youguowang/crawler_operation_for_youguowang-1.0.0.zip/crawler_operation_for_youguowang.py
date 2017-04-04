import re
import requests
import os
import time
from bs4 import BeautifulSoup
from random import randint

lines = (
    '请问你是喜欢《兽娘动物园》的朋友吗？~',
    'すごーい!( ﾟ∀。)',
    'たーのしー！(●ˇ∀ˇ●)',
    "面白い！(●'◡'●)",
    'LALALALALALALALALA~~~',
    '你是擅长什么的朋友呢？',
    '要调教什么的，别说出这么让人兴奋的话嘛',
    '真不愧是我啊~',
    '越是珍惜呆在这里的时间，今后就越是悲伤吧。但是我认为不能称之为「后悔」',
    '啊……是主人~快进来~',
    '当然不，仁慈的先生！我到这儿只为打扫您的房间',
    '我不懂您的暗示，主人。我只是个女仆，如此可怜',
    '但它太过硕大！要浪费我整整一夜！',
    '上帝啊，真是一大条面包！可如何才能把它塞进我的炉中烘烤？',
    '就在这儿？您希望我揉捏这块面包？',
    '可女主人抓住我怎么办？你的面包本该用来满足她的嗜好。',
    '好吧，可我还担心我的炉子不够火热，要烤几个小时的面包！',
    '咳、咳咳！What is better - to be born good, or to overcome your evil nature through great effort?',
    '何为上：生而为善，亦或是通过努力摒除恶念？',
    '（深呼吸）.....你的剑比你的兄弟更加锋利..…更加有穿透力......但是你的儿子却像一个诺德的枪骑兵一样勇猛！',
    '呼呼~主人，小豆累了呢，让小豆休息一会......',
    '今天你陪着我好么？好像有点冷呢。',
    '啊，这烟花好漂亮啊，可是，烟花下的你，却让我无法专心去欣赏呢。',
    '假如樱花飘落的速度是秒速五厘米，那我的心想飞到你身边的速度就是秒速五光年。',
    '这世界很大，我们却很小，但你散发的光芒，能照亮整个世界!!!',
    '我这辈子最大的希望就是吃饭吃到饱，睡觉睡到饱~',
    '人要是没有梦想，和咸鱼有什么区别！',
    '生活就是这样，不像一首诗，转身撞到了现实，只能如是了......',

)



# 函数功能：
# 爬取所有进入组图的链接
# 接收参数：
# url--包含组图链接的页面链接，headers--请求头
# 返回值：
# link_list--包含所有组图链接的列表
def find_entrance_link(url, headers):
    response = requests.get(url, headers = headers, stream = True)
    #print(response.encoding)    测试用
    #print(response.apparent_encoding)    测试用
    response.encoding = response.apparent_encoding
    bs_object = BeautifulSoup(response.text, "html.parser")
    #print(bs_object.get_text())    测试用
    # .findAll()返回的是一组标签
    entrance_link_set = bs_object.findAll("a",{"href":re.compile("http://www.meitulu.com/item/\d+[.]html")})
    link_list = list()
    for temp_link in entrance_link_set:
        #print(temp_link)   #测试用
        # 此处["href"]是将标签中 "href"属性对应的值(即链接)截取出来
        if not temp_link["href"] in link_list:
            #发现了不在链接集里的列表，或者不重复的链接，则将其加入链接列表
            link_list.append(temp_link["href"])
            #print("找到一个新连接~")
    return link_list



# 函数功能：
# 爬取所有高清原图的链接
# 接收参数：
# url--包含原图链接的页面链接，headers--请求头
# 返回值：
# img_link_list--包含所有原图链接的列表
def find_img_link(url, headers):
    html = requests.get(url, headers = headers, stream = True).text
    html_trans = BeautifulSoup(html, "html.parser")
    img_link_no_trans = html_trans.findAll("img",{"class":"content_img"})
    img_link_list = list()
    for temp_link in img_link_no_trans:
        img_link_list.append(temp_link["src"])
    return img_link_list



'''
有bug 已淘汰
# 函数功能：
# 爬取进入该组图的下一页的链接
# 接收参数：
# url--当前页面的链接，headers--请求头
# 返回值：
# next_link--进入下一页的链接
def find_next_link(url, headers):
    response = requests.get(url, headers = headers, stream = True)
    response.encoding = response.apparent_encoding
    html = response.text
    html_trans = BeautifulSoup(html, "lxml")
    next_link_no_trans = html_trans.findAll("a", {"class":"a1"})
    flag = str("下一页")
    next_link = str()
    for temp_link in next_link_no_trans:
        #print(temp_link.get_text()) 测试用
        if temp_link.get_text() == flag:
            next_link = temp_link["href"]
            break
    return next_link
'''



# 函数功能：
# 保存高清原图
# 接收参数：
# url--原图的链接，headers--请求头，root--存放图片的文件夹路径
# 返回值：
# 正常保存返回 0 ；文件存在返回 1； 异常抛出返回 2；
def save_img(url, headers, root):
    response = requests.get(url, headers=headers, stream=True)
    path = root + url.split('/')[-1]
    #print(path) 测试用
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            with open(path,'wb') as f:
                f.write(response.content)
                f.close
                print("文件保存成功")
                robot_lines()
                return 0
        else:
            print("文件已经存在")
            return 1
    except:
        print("爬取失败")
        return 2



# 函数功能：
# 检测该组图的最大页数；
# 也可以检测组图页最大页数；
# 接收参数：
# url--该组图内任意一页的链接，headers--请求头
# 返回值:
# max_page--最大页数(int 型)
def find_max_page(url, headers):
    max_page = -1
    response = requests.get(url, headers=headers, stream=True)
    response.encoding = response.apparent_encoding
    html = BeautifulSoup(response.text, "html.parser")
    sum_of_page = html.findAll("a", string=re.compile("^\d+$"))
    '''
    测试用
    test = html.findAll("span", string = re.compile("^\d+$"))
    for i in test:
        print("span is ", i.string)
    '''
    for temp_num in sum_of_page:
        if max_page < int(temp_num.string):
            max_page = int(temp_num.string)
    # print(number)    测试用
    return max_page



# 函数功能：
# 检测当前页面所在页数
# 接收参数：
# url--当前页面的链接，headers--请求头
# 返回值：
# current_page--当前所在页面（int 型）
def detection_current_page(url, headers):
    response = requests.get(url, headers = headers, stream = True)
    response.encoding = response.apparent_encoding
    html = BeautifulSoup(response.text, "html.parser")
    current_page = int(html.find("div",{"id":"pages"}).span.string)
    #print(current_page)    测试用
    return current_page



# 函数功能：
# 查询当前所在组图页的页码
# 接收参数：
# url--所在页面的链接，headers--请求头
# 返回值：
# current_page--所在页码（int 型）
def detection_group_current_page(url, headers):
    response = requests.get(url, headers = headers, stream = True)
    response.encoding = response.apparent_encoding
    html = BeautifulSoup(response.text, "html.parser")
    current_page = int(html.find("div",{"id":"pages"}).span.string)
    #print(direction_span)    测试用
    return current_page


# 函数功能：
# 爬取通向当前页面的下一页的链接
# 接收参数：
# url--当前页面的链接，headers--请求头
# 返回值：
# next_page_link--下一页的链接（str 型）
def find_next_page_link(url, headers):
    current_page = detection_current_page(url, headers)
    #测试用
    #print(current_page)
    #print("next page is ", current_page + 1)
    response = requests.get(url, headers = headers)
    response.encoding = response.apparent_encoding
    html = BeautifulSoup(response.text, "html.parser")
    next_page_link = str(html.find("a", string = str(current_page + 1))["href"])
    #print(next_page_link)    测试用
    return next_page_link



# 函数功能：
# 寻找组图页的下一页链接
# 接收参数：
# url--当前所在组图页的链接，headers--请求头
# 返回值：
# next_group_page_link--下一页组图页的链接（str 型）
def find_next_group_page_link(url, headers):
    current_page = detection_group_current_page(url, headers)
    #测试用
    #print(current_page)
    #print("next page is ", current_page + 1)
    response = requests.get(url, headers = headers)
    response.encoding = response.apparent_encoding
    html = BeautifulSoup(response.text, "html.parser")
    next_group_page_link = str(html.find("a", string = str(current_page + 1))["href"])
    #print(next_group_page_link)    #测试用
    return next_group_page_link



# 函数功能
# 控制爬取的时间间隔；随机打印台词；
# 无参
# 无返回值
def robot_lines():
    lines_len = len(lines)
    print(lines[randint(0,lines_len - 1)])
    time.sleep(1)