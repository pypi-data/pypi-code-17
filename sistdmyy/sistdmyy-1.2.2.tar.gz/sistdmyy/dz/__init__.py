import pandas as pd

import numpy as np

import re
from sistdmyy.dz.dz_jd import jd_predict,jdtrain
from sistdmyy.dz.dz_std import std


#mine是用来生成dz_dz表的
'''
这个类主要接口是dz_dasa 返回地理名词
dz_dasa("深圳市盐田区沙深路粤和街13号稳胜大厦A栋五楼左侧503室",'大厦')=稳胜大厦

pats()生成一个类变量P P['大厦']=[关于该名词的正则规则]

minedf(df['jgdz']) 形成一个 type-word-tag-tf的表

'''
class mine:
    def __init__(self):

        self.dot1=["大厦","大楼","社区","路","大道","工业园","工业区","科技园","小区","花园","苑","公寓","村","公馆",'广场','道','华庭','豪庭']
        self.aso={'大厦':"楼群","大楼":"楼群","社区":"村社镇","路":"路道街","大道":"路道街","工业园":"楼群","工业区":"楼群","科技园":"楼群","小区":"楼群"
                ,"花园":"楼群","苑":"楼群"
                ,"公寓":"楼群","村":"村社镇","公馆":"楼群","广场":"楼群","道":"路道街","华庭":"楼群","豪庭":"楼群"}
        self.pat('路')
        self.pats()

    def pat(self,target):
        self.dot=["路路口"
            ,"路口"
            ,"路路[东南西北]"
            ,"路\d+"
            ,"路向[东南西北]"
            ,"路"
            ,"办事处"
            ,"街道办"
            ,"街道\d*"
            ,"街\d*"
            ,"大道\d*"
            ,"交界处"
            ,"交汇处"
            ,"[东西南北]侧"
            ,"与"
            ,"对面"
            ,"交叉口"
            ,"[0-9一-十]号"
            ,"[东南西北]{2}角"
            ,"旁"
            ,"[0-9一-十a-zA-Z东南西北]部"
            ,"村"
            ,"[0-9一-十a-zA-Z]栋"
            ,"[0-9一-十a-zA-Z]区"
            ,"[0-9一-十a-zA-Z]巷"
            ,"[0-9一-十a-zA-Z东南西北]门"
            ,"[0-9一-十a-zA-Z东南西北]幢"
            ,"附近"
            ,"[0-9一-十a-zA-Z东南西北]侧"
            ,"大厦"
            ,"社区"
            ,"小区"
            ,"科技园"
            ,"花园"
            ,"工业园"
            ,"苑"
            ,"[东西南北]{2}"
            ,"广场"
            ,"大楼"
            ,"(?:龙华新|龙岗|南山|福田|罗湖|盐田|光明新|宝安|坪山新|大鹏新|合作)区"
            ,"深圳市"
            ,"交接处"
            ,"以[东南西北]"
            ,"城(?<!市)"
            ,"厂房"
            ,'的'
            ,'与'
            ]
        self.ss1=list(map(re.compile,map(lambda x:"%s([^\d口村路区栋巷号门\-][^村路区栋巷号门]{1,4}%s)"%(x,target),self.dot)))

    def pats(self):
        self.p={}
        for w in self.dot1[:-5]:
            self.p[w]=list(map(re.compile,map(lambda x:"%s([^\d口村路区栋巷号门\-][^村路区栋巷号门]{1,4}%s)"%(x,w),self.dot)))
        self.p['公馆']=list(map(re.compile,map(lambda x:"%s([^\d口村路区栋巷号门\-][^村路区栋巷号门]{1,3}%s)"%(x,'公馆'),self.dot)))
        self.p['广场']=list(map(re.compile,map(lambda x:"%s([^\d口村路区栋巷号门\-][^村路区栋巷号门]{1,4}%s)"%(x,'广场'),self.dot)))
        self.p['道']=list(map(re.compile,map(lambda x:"%s([^\d口村路区栋巷号门\-][^村路区栋巷号门街大]{1,3}%s)"%(x,'道'),self.dot)))
        self.p['华庭']=list(map(re.compile,map(lambda x:"%s([^\d口村路区栋巷号门\-][^村路区栋巷号门]{1,2}%s)"%(x,'华庭'),self.dot)))
        self.p['豪庭']=list(map(re.compile,map(lambda x:"%s([^\d口村路区栋巷号门\-][^村路区栋巷号门]{1,2}%s)"%(x,'豪庭'),self.dot)))
        #东门中路出不来
        self.p['路'].extend(list(map(re.compile,map(lambda x:"%s([^\d口村路区栋巷号门\-][^村路区栋巷号]{1,3}%s)"%(x,'路'),self.dot))))
    def dz_dasa(self,a,w):
        if a is None:return ''
        a= re.sub("[\s+\.\!\/_,$%^*(+\"\';]+|[+——！，。？、~@#￥%……&*（）\[\]；;]+", "",a)
        for s in self.p[w]:
            b=s.search(a)
            if b is None:
                continue
            else :
                b=b.group(1)
                for s1 in self.p[w]:
                    c=s1.search(b)
                    if c is None:
                        continue
                    else:
                        c=c.group(1)
                        return  c
                return b
            
        return None
    def dz_dasa3(self,a):
        if a is None:return ''
        a= re.sub("[\s+\.\!\/_,$%^*(+\"\';]+|[+——！，。？、~@#￥%……&*（）\[\]；;]+", "",a)
        for s in self.ss1:
            b=s.search(a)
            if b is None:
                continue
            else :
                b=b.group(1)
                for s1 in self.ss1:
                    c=s1.search(b)
                    if c is None:
                        continue
                    else:
                        c=c.group(1)
                        return  c
                return b
            
        return ''
    #通过字典来形成地理名词表
    def minedf(self,df):
        #df=["深圳市盐田区沙深路粤和街13号稳胜大厦A栋五楼左侧503室"]
        ds=[]
        for word in df:
            d,d1={},{}
            for w in self.dot1:
                x=self.dz_dasa(word,w)
                if x is not None and x!='':d[w]=x
            if d=={}:continue
            for w1,w2 in d.items():
                d1['type'],d1['word'],d1['tag']=w1,w2,self.aso[w1]
                ds.append(d1)
                d1={}
        df1=pd.DataFrame(ds)
        df2=df1.groupby(list(df1.columns)).size()
        data=[df2.index.get_level_values(i) for i in range(3)]
        data.append(df2.values)
        col=list(df1.columns)
        col.append('tf')
        df3=pd.DataFrame(np.array(data).transpose(),columns=col)

        return df3


    def strQ2B(self,ustring):
        """把字符串全角转半角"""
        rstring = ""
        for uchar in ustring:
            inside_code=ord(uchar)
            if (inside_code >= 0x0021 and inside_code <= 0x7e)  :   #全角直接返回
                rstring += uchar
            else:
                if inside_code==0x3000:                         #全角角空格单独处理 
                    inside_code = 0x0020
                else:                                           #其他的全角半角的公式为:半角 = 全角- 0xfee0
                    inside_code -= 0xfee0
                
                rstring += chr(inside_code) if inside_code  in range(0x110000)  else uchar     
        return rstring

    def clear_bracket1(self,a):

        b=re.sub("\([^\(]*?\)",'',a)
        b=re.sub("\([^\(]*?\)",'',b)
        return b

    def clear_bracket(self,a):
        #'''#[] “” 【】 ()'''
        b=re.sub("(?:\([^\(]*?\))|(?:\[[^\[]*?\])|(?:【[^\【]*?】)|(?:“[^“]*?”)",'',a)
        b=re.sub("(?:\([^\(]*?\))|(?:\[[^\[]*?\])|(?:【[^\【]*?】)|(?:“[^“]*?”)",'',b)
        return b
    #标点分割
    def tpunctuation(self,a):
        b = re.sub("[\s+\.\!\/_,$%^*(+\"\';]+|[+——！，。？、~@#￥%……&*（）\[\]]+", ";",a)
        ##!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
        return b

    def clear(self,a):
        a=self.strQ2B(a)
        a=self.clear_bracket(a)
        #a=self.tpunctuation(a)
        return a
    def clear_mine(self,a):
        return self.dz_dasa3(self.clear(a))
#def mine_selected(self):
#    sql="select top 1000 jgdz from basedb.dbo.t_zzjgjz where jgdz is not null order by newid()"
#    m=db()
#    df=m.frommssql(sql)
#    df1=self.minedf(df['jgdz'])
#    return df1


