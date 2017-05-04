# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 08:52:15 2017

@author: Yuki
"""

#プログラムの状態
INITIAL=0   #最初の状態　ファイルが指定されていない
READY=1     #ファイルが入力され、かつ指定された測定器が見えている状態
NOTFOUND=2  #ファイルが入力され、指定された測定器が見つからない状態
RUNNING=3   #測定プログラムが走っている状態