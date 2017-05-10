# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 16:42:39 2017

@author: liujiacheng1
"""
import pandas as pd
import time
from cluster import cluster  
from clean_data import news_cover2
from news_len import news_cover_func



time=str(time.time())



def process(time):
    #loading data
    attention=pd.read_excel('raw_attention.xlsx')
    stock_ratios=pd.read_excel('RAW_stocks1.xlsx')
    industry=pd.read_excel('Raw_industry.xlsx')
    news=news_cover_func(time,news_cover2)
    news=pd.DataFrame(news,dtype='float64')
    
    print(news)
    #merge ratios with raw_attention
    c=pd.merge(attention,stock_ratios,how='inner',on='index')
    c.to_csv('merged'+time+'.csv')
    
    
    
    
    #merge the datasets wiith industry code
    with_ind=pd.merge(c,industry,how='left',on='index')
    #with_ind.to_csv('ssss.csv')
    
    
    #merge news_coverage
    
    with_news=pd.merge(with_ind,news,how='left',on='index') 


    
    #groupby functions
    result_grouped=with_news.groupby('pin').mean() 
    
    
    
    #stock with news
        
    stock_news=pd.merge(stock_ratios,news,how='right')
    stock_news.to_csv('stock_news'+time+'.csv')
    print(news.dtypes)
    print(stock_news.dtypes)
    
    print(stock_news.dtypes)
    
    #correlation stock_news
    
    





                    
                                         
    #pure_ratios
    #generating the data sets with pure ratios to avoiod the encoding problems
    pure_ratios=result_grouped.iloc[:,6:]
    pure_ratios=pure_ratios.reset_index(drop=True)
    pure_ratios=pure_ratios.fillna(value=0)
    pure_ratios.to_csv('process_pure'+time+'.csv',index=False)
    
    
    
    #select specific colunms
    first_half=result_grouped.iloc[:,:0]
    second_half=result_grouped.iloc[:,6:]
    pieces=[first_half,second_half]
    results_with_index=pd.concat(pieces,1)
    results_with_index.to_csv('process'+time+'.csv',encoding='utf-8')
    
    
    
    
    #raw_pure_ratios=pd.concat(pieces_pure_ratios,1)
    #generating the data sets with pure ratios to avoiod the encoding problems
    #merge with industry data

    #e=pd.merge(c,d,how='left',on='index')

    #e.to_csv('merged_ind'+time+'.csv')
    
    
    
    

process(str(time))
cluster(30,str(time),'complete')