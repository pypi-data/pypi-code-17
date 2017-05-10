#!/usr/bin/env python
#-*-coding:utf-8-*-

# author : "qiulimao"
# email  : "qiulimao@getqiu.com"

""" 
 模型训练
""" 
#---------- code begins below -------
import re
import numpy as np
from matplotlib import pyplot as plot
import pyquery
from lxml.html import fromstring,tostring

class Training(object):
    """
    """

    def __init__(self):
        

        self.P_tagmap_Y = []
        self.P_tagmap_N = []
        
        self.P_density_Y = []
        self.P_density_N = []

        self.P_similarity_Y = []
        self.P_similarity_N = []
        

    @property
    def focused_tag(self):
        """
            关注的标签内容
        """
        return ["p","a","span","li","strong","font","pre"]

    def __tagfunc_traning(self,node):
        """
            标签作用训练
        """
        return node.tag


    def __density_traning(self,node,text_content=False):
        """
            密度训练,
            text_content 可选，如果选择text_content=True,
            那么将会选择一个标签下的所有文本
        """
        pure_text = node.text_content() if text_content else node.text

        return len(pure_text) if pure_text else 0


    def __similarity_traning(self,node):
        """
            相似度训练
        """
        tag_name = node.tag
        parent = node.getparent()
        #if not parent:
        #    return 0

        similaritys = len(parent.xpath("./%s" % tag_name))

        return similaritys



    def __get_html_leaves(self,htmlsource):
        """
            获取html 文档当中的DOM
        """
        pyquery_dom = pyquery.PyQuery(htmlsource)
        pyquery_dom("style").remove()
        pyquery_dom("script").remove()
        html_dom = fromstring(pyquery_dom.html())
        ##
        # 以下两句话就是想构造一个xpath selector
        # 比如 "//p | //a | //span | //ul | //li | //font | //strong | //pre | //em"
        ##
        xpath_locator = reduce(lambda t1,t2:t1+"|//"+t2,self.focused_tag)
        xpath_locator =  "//"+xpath_locator
        return html_dom.xpath(xpath_locator)

    
    def __the_node_is_a_leaf(self,node):
        """
            当前节点是否为叶子节点
        """
        return False if len(node.getchildren()) > 0 else True
            
    def _training(self,training_source,note="",text_content=False,skip_non_leaf_node = False,show_figure=True,laplace_correct=True):
        """
            training_source: 设置源
            note 设置画图标记
            skip_non_leaf_node :跳过非叶子节点
            show_figure: 显示图像
            laplace_correct: 设置拉普拉斯矫正
            需要训练的向量有：
                *   标签的概率统计
                *   密度的概率统计
                *   相似度的概率统计
        """
        # 标签出现次数
        tag_show_up_times = dict()
        density_for_every_tag = []    # 这个数组是为了用来画密度直方图
        similarity_for_every_tag = [] # 这个数组是为用来画 标签相似度直方图
        sizeof_training_sample = 0
        map(lambda t:tag_show_up_times.__setitem__(t,0.0),self.focused_tag)
        
        for node in training_source:
            ##
            # 是否跳过过非叶子节点
            ##
            if skip_non_leaf_node and not self.__the_node_is_a_leaf(node):
                continue
            ##
            # 统计总共有多少个tag
            ##
            sizeof_training_sample += 1

            ##
            # 统计标签用途
            ##
            tag_name = self.__tagfunc_traning(node)
            tag_show_up_times[tag_name] += 1

            ##
            # 统计密度
            ##
            density = self.__density_traning(node,text_content)
            density_for_every_tag.append(density)

            ##
            # 兄弟节点相似性
            ##
            similarity = self.__similarity_traning(node)
            similarity_for_every_tag.append(similarity)
            
        ##
        # 到此 三个重要向量的原始数据就统计完了，接下来就该计算出相关的条件概率了
        ##
        plot.figure(figsize=(8,10)) 
        plt_tag = plot.subplot(311)
        plt_density = plot.subplot(312)
        plt_similarity = plot.subplot(313)


        ##
        # 标签作用
        ##
        tag_show_up_possibility = dict()
        for k,v in tag_show_up_times.items():
            tag_show_up_possibility[k] = float(v) / sizeof_training_sample
        

        ##
        # 统计密度直方图直方图统计
        ##
        n,bins,pathces = plt_density.hist(density_for_every_tag,bins=map(lambda x:x-0.5,range(1,100)),facecolor='yellowgreen')
        density_possibility = map(lambda t:float(t)/sizeof_training_sample,n)


        ##
        # 统计相似性概率分布图
        ##
        sn,sbins,npathes = plt_similarity.hist(similarity_for_every_tag,bins=map(lambda x:x-0.5,range(1,100)))
        similarity_possibility = map(lambda t:float(t)/sizeof_training_sample,sn)

        ##
        # 启用拉普拉斯 修正
        ##

        if laplace_correct:
            self.__laplace_correct(tag_show_up_possibility,sizeof_training_sample)
            self.__laplace_correct(density_possibility,sizeof_training_sample)
            self.__laplace_correct(similarity_possibility,sizeof_training_sample)

        ##
        # 最终返回数据
        ##
        statistics = {"sample_count":sizeof_training_sample,"tag_possibility":tag_show_up_possibility,
                "density_possibility":density_possibility,"similarity_possibility":similarity_possibility}

        ##
        # 设置画图相关属性，不用理会
        ##
        if show_figure:
            plt_tag.bar(np.arange(len(tag_show_up_times))+0.25,tag_show_up_times.values(),width = 0.35,facecolor='red',alpha=0.75)
            plt_tag.set_xticks(np.arange(len(tag_show_up_times))+0.5)
            plt_tag.set_xticklabels(tag_show_up_times.keys())
            plt_tag.set_title("tag show up times for %s" % note)
            # 画图相关设置
            plt_density.set_title("text density for %s" % note)
            # 画图相关设置
            plt_similarity.set_title("label similarity in sblings for %s" % note)
            plot.show()

        return statistics
    
    def __laplace_correct(self,data,sample_amount):
        """
            拉普拉斯修正
        """
        if isinstance(data,list):
            for i in range(0,len(data)):
                if data[i] <= 0:
                    data[i] = float(1)/sample_amount

        elif isinstance(data,dict):
            for k,v in data.items():
                if v <= 0.0:
                    data[k] = float(1)/sample_amount
        return data

    def training_for_noise(self):
        """
            噪音训练器
        """
        
        result = self._training(self.negetive_training_source(),note="noise",text_content=True,skip_non_leaf_node=True)
        return result

    def training_for_content(self):
        """
            外部调用
        """
        result = self._training(self.positive_training_source(),note="content",text_content=True,skip_non_leaf_node=True)
        return result

    def positive_training_source(self):
        """
            正向训练样本生成器,必须返回一个lxml中<HTMLElement>对象
            override this method.
        """
        from models import WebContent,to_session

        webcontents = to_session.query(WebContent).limit(800).all()
        for one_content in webcontents:
            try:
                leaves = self.__get_html_leaves(one_content.content)
                for leaf in leaves:
                    yield leaf
            except TypeError:
                continue
            except Exception:
                continue
    
    def negetive_training_source(self):
        """
            负向训练样本生成器,必须返回一个lxml中<HTMLElement>对象
            override this method.
        """
        from models import WebContent,to_session

        webcontents = to_session.query(WebContent).limit(400).all()
        for one_content in webcontents:
            try:
                leaves = self.__get_html_leaves(one_content.noise)
                for leaf in leaves:
                    yield leaf
            except TypeError:
                continue
            except Exception:
                continue




if __name__ == "__main__":
    """
        
    """
    trainner = Training()
    result = trainner.training_for_content()
    print result