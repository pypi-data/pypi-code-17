# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 11:00:13 2017

@author: liujiacheng1
"""
import tushare as ts
import pandas as pd
import numpy as np

from time import time
from sklearn import linear_model
from sklearn import preprocessing
from indexs import sh50, all_stocks, test


# global setting


results = []

selected_results = []

time = str(time())


def regress(index, benchmark, time):
    global remaining_min, remaining_min
    a = ts.get_hist_data(benchmark)
    a = pd.DataFrame(a)

    a = a.reset_index()

    # print(a)

    b = ts.get_hist_data(index)
    b = pd.DataFrame(b)
    b = b.reset_index()
    # print(b)




    c = pd.merge(a, b, how='inner', on='date')
    # x stands for benchmark
    # y stands for index


    df = c
    price_change_benchmark = df['p_change_x']
    price_change_index = df['p_change_y']

    print(c)

    ############################
    # global data

    Trading_days = len(df['p_change_y']) - 1

    Annually_time = Trading_days / 360

    ###########################
    # yield
    ###########################


    total_yield_index = (df.iloc[0, 16] - df.iloc[len(price_change_index) - 1, 16]) / df.iloc[0, 16]

    Daily_yield_index = total_yield_index / Trading_days

    Annual_yield_index = total_yield_index / Annually_time

    total_yield_benchmark = (df.iloc[0, 4] - df.iloc[len(price_change_benchmark) - 1, 4]) / df.iloc[0, 4]

    Daily_yield_benchmark = total_yield_benchmark / Trading_days

    Annual_yield_benchmark = total_yield_benchmark / Annually_time

    #############################


    # Regress alpha beta
    #############################
    regr = linear_model.LinearRegression()

    regr.fit(price_change_benchmark.reshape(-1, 1), price_change_index)
    
    b, a = regr.coef_, regr.intercept_

    alpha = a

    beta = str(b).strip('[').strip(']')

    ##################################


    # Risk
    ##################################




    varance_benchmark = np.var(df['p_change_x'])

    varance_index = np.var(df['p_change_y'])

    neg_changes = []
    for i in range(1, len(df['p_change_y'])):
        if c.iloc[i, 20] < 0:
            neg_changes.append(c.iloc[i, 20])
    downside_risk = np.var(neg_changes)

    ##########################
    # max withdraw(calculating in part 2)
    ###########################
    # def max_withdraw():


    # print(np.argmax(df['close_y']))
    # print(np.argmin(df['close_y']))

    max_benchmark = np.argmax(df['close_y'])
    min_benchmark = np.argmin(df['close_y'])

    if min_benchmark < max_benchmark:
        Max_withdraw = (max_benchmark - min_benchmark) / max_benchmark


    else:

        withdraws = []

        for i in range(1, Trading_days):

            remaining = df['close_y'][i:]

            # remaining_days=Trading_days-i
            try:
                remaining_min = np.amin(remaining)
            except:
                pass
            withdraw = (df.iloc[i, 16] - remaining_min) / df.iloc[i, 16]

            withdraws.append(withdraw)

        Max_withdraw = np.amax(withdraws)

    ######################################
    # active
    # #########################################

    active_risk = varance_index - varance_benchmark

    # active_profit=np.average(df['p_change_y']-df['p_change_x'])
    active_profit_daily = Daily_yield_index - Daily_yield_benchmark

    active_profit_annual = Annual_yield_index - Annual_yield_benchmark

    active_profit_total = total_yield_index - total_yield_benchmark

    #########################################
    # style


    ####################################
    win = 0
    for i in range(1, len(df['p_change_y'])):
        if c.iloc[i, 20] > 0:
            win += 1

    win_rate = win / len(price_change_index)

    ######################################
    # Var
    ######################################
    # Var5=np.percentile(df['p_change_y'],0.05)
    # Var2=np.percentile(df['p_change_y'],0.02)

    Var10 = np.percentile(df['p_change_y'], 10)
    # Var20=np.percentile(df['p_change_y'],0.2)

    # Var30=np.percentile(df['p_change_y'],3)
    # Var40=np.percentile(df['p_change_y'],4)

    Var5 = np.percentile(df['p_change_y'], 5)

    #################################

    # print results

    ###################################

    result = {'index': index, 'alpha': alpha, 'beta': beta, 'varance': varance_index, 'win_rate': win_rate,
              'active_risk': active_risk, 'downside_risk': downside_risk, 'Var10': Var10, 'Var5': Var5,
              'total_yield': total_yield_index, 'Daily_yield': Daily_yield_index, 'Annual_yield': Annual_yield_index,
              'Max_withdraw': Max_withdraw, 'active_profit_daily': active_profit_daily,
              'active_profit_annual': active_profit_annual, 'active_profit_total': active_profit_total}

    selected_result = {
        'index': index,

        'alpha': alpha,

        'beta': beta,

        'varance': varance_index,

        'win_rate': win_rate,

        'active_risk': active_risk,

        'downside_risk': downside_risk,

        'Var10': Var10,

        'total_yield': total_yield_index,

        'Max_withdraw': Max_withdraw,

        'active_profit_daily': active_profit_daily}

    results.append(result)

    selected_results.append(result)
    # print("(",'"index":',index,',','"alpha":',a,',','"beta":',beta,')')
    # print(results)
    # print(c.iloc[i,20])


    now_results = pd.DataFrame(results)

    # min_max_scaler = preprocessing.MinMaxScaler()
    # results_tansformed= min_max_scaler.fit_transform()

    print(now_results)
    # print(df.iloc[0,16],df.iloc[len(df['p_change_y'])-1,16])

    now_results.to_csv('C:/Users/liujiacheng1/Desktop/py/backupljc/' + index + time)

    # start calculating max withdraws
    # print('First Part complete,start calculating second part')




    ################################


# runner
###########################
def run(sort, time):
    for index in sort:
        regress(index, 'sh', time)
    
    final_results = pd.DataFrame(results)
    final_results.to_excel('Ratio_result' + time + '.xlsx')

    print(final_results)

    # description
    des = final_results.describe()
    des.to_csv('describe' + time + '.csv')
    print(des)


    print('OK')


# regress('000001','sh')
# run(all_stocks,time)
run(test, time)