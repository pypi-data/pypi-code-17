# -*- coding: utf-8 -*-

"""
Created on Sat Jan 21 10:01:17 2017

@author: lby
"""
from tqdm import *
from .mis import *
from urllib.request import urlopen
from bs4 import BeautifulSoup

import datetime as dt
import re
import pandas as pd
import time

URL_BASE = 'http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?'

def get_future_codes(jys = 'all'):
	sqs = ['rb','wr','cu','al','ru','fu','zn','au','ag','bu','hc','ni','pb','sn']
	dss = ['a','b','bb','c','cs','fb','i','j','jd','jm','l','m','p','pp','v','y']
	zss = ['cf','fg','jr','lr','ma','oi','ri','rm','rs','sf','sm','sr','ta','wh','zc']
	zjs = ['IF','TF','IH','IC']
	future_codes = [sqs,dss,zss,zjs]
	df = pd.DataFrame(future_codes).T
	df.columns = ['sqs','dss','zss','zjs']

	if jys == 'all':
		return df
	else:
		return df[jys]

def sina_url_cal(code,hy = 0, start = '', end = ''):
	df = get_future_codes()
	df.columns = [('sqs','1'),('dss','2'),('zss','3'),('zjs','4')]

	dft = df[df == code].dropna(how='all').dropna(axis = 1)

	if hy == 0:
		code += '0'

	url = URL_BASE + 'jys=' + dft.columns[0][1] + '&pz=' + str(dft.iloc[0].name) + '&hy=' + str(hy) + '&breed=' + code + '&start=' + start + '&end=' + end
	return url

def read_zip_url(url):
	fails = 0
	max_times = int(5e1)
	while fails < max_times:
		try:
			html = urlopen(url)
			break
		except:
			fails += 1
		print('occused error, retrying' + str(fails) + '/' + str(max_times) + 'times')

	bsObj = BeautifulSoup(html, "lxml")
	return bsObj

def future_data_clean(bsObj):
	#print(bsObj)
	his = bsObj.find('div',{'class':'historyList'})
	data = his.findAll('div',{'align':'center'})
	data = pd.DataFrame(data,columns = ['text'])
	data['text'] = data['text'].astype(str).str.replace('<div align="center">','')
	data['text'] = data['text'].astype(str).str.replace('</div>','')
	data['text'] = data['text'].astype(str).str.replace('<strong>','')
	data['text'] = data['text'].astype(str).str.replace('</strong>','')

	# when update with no data:
	if len(data) <= 6:
		col_num = 6
		df = pd.DataFrame([],columns = data[:col_num]['text'].tolist())
		return df


	if data.loc[6]['text'] == '持仓量':

		col_num = 7
	else:
		col_num = 6
	df = pd.DataFrame(list(zip(*[iter(data[col_num:]['text'])]*col_num)),columns = data[:col_num]['text'].tolist())

	return df

def get_pages_url(bsObj):
	a = bsObj.find('a',text = '尾页')
	if a == None:
		return
	a = a.attrs['href']
	x = int(re.findall('page=\d+',a)[0].replace('page=',''))

	p = 'page='
	u = a[a.find(p):]
	u = re.sub(p + str(x),'',u)
	u = re.sub('&name=.*','',u)

	res = []
	for i in range(2,x+1):
		ut = URL_BASE + p + str(i) + u
		res.append(ut)
	return res

def get_data_from_url(url):
	bsObj = read_zip_url(url)
	df = future_data_clean(bsObj)
	return df
def get_future_data(code,hy = 0, date = '', start = '', end = '',num = 30):

	today_date = dt.datetime.now().strftime('%Y-%m-%d')

	if date != '':
		start = date
		end = date
	elif start == '':
		if end == '':
			date30 = pd.date_range(end = today_date,periods = num)
		else:
			date30 = pd.date_range(end = end,periods = num)
		start = date30.to_datetime().strftime('%Y-%m-%d').tolist()[0]
		end = date30.to_datetime().strftime('%Y-%m-%d').tolist()[-1]
	elif end == '':
		end = today_date

	url = sina_url_cal(code = code,hy = hy, start = start, end = end)
	bsObj = read_zip_url(url)
	df = future_data_clean(bsObj)

	url_list = get_pages_url(bsObj)
	#print(df)
	#print('#', end='')

	if url_list != None:
		for u in tqdm(url_list):
			#print(u)
			dft = get_data_from_url(u)
			#print(dft)
			df = df.append(dft)

	#print(df)

	df[df.columns[1:]] = df[df.columns[1:]].astype(float)

	if len(df.columns) == 7:
		df.columns = ['date','close','open','high','low','volume','position']
	if len(df.columns) == 6:
		df.columns = ['date','close','open','high','low','volume']
	df = df.sort_values('date')
	df.index = pd.to_datetime(df['date'])
	del df['date']
	return df

"""df = get_future_data('ta',start = '2017-01-01', end = '2017-04-19')
print(df)
df = get_future_data('ta',date = '2016-06-01')
print(df)
df = get_future_data('ta',start = '2014-01-01')
print(df)"""
#

def future_data_initialize(host = ''):
	#if host == '':
	#	print('Attention, please specify the cloud ip !')
	#	return
	dfc = get_future_codes(jys = 'all')
	for col in tqdm(dfc.columns[:]):
		print(col)
		for code in tqdm(dfc[col]):
			if code != None:
				print(code)
				df = get_future_data(code,start = '1980-01-01')
				df_to_sql('future',code.lower() +'_day',df,option = 'append',host=host)


def future_update_code(code,host = ''):
	#if host == '':
	#	print('Attention, please specify the cloud ip !')
	#	return
	strq="SELECT MAX(date) FROM %s_day;" % code
	dfd = sql_to_df('future',strq,host = host)
	new_start = (dfd.iloc[0]['MAX(date)'] + dt.timedelta(days=1)).strftime("%Y-%m-%d")
	timenow = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print(timenow,code,new_start)
	dfn = get_future_data(code, start=new_start)
	df_to_sql('future',code.lower() +'_day',dfn,option = 'append',host=host)

def future_update_all(host = ''):
	#if host == '':
	#	print('Attention, please specify the cloud ip !')
	#	return
	dfc0 = get_future_codes(jys = 'all')
	strq = "SHOW TABLES;"
	dfc = sql_to_df('future',strq,host = host )
	for code in dfc['Tables_in_future']:
		code = code[:-4]
		if code.upper() in dfc0['zjs'].tolist():
			code = code.upper()
		future_update_code(code,host = host)

if __name__ == '__main__':
	future_update_all(host = '')
