# -*- coding: gb2312 -*-

"""
Created on Tue Oct 25 15:40:37 2016

@author: lby
"""

import datetime as dt
import pandas as pd
import tushare as ts
import urllib

def get_etick_data(code,date = ''):
	if date == '':
		date = dt.datetime.now().strftime('%Y-%m-%d')
	if code[0:1]=='6':
		code ='0' + code
	else:
		code ='1' + code

	url='http://quotes.money.163.com/cjmx/%s/%s/%s.xls' % (date.replace('-','')[:4],date.replace('-',''),code)
	try:
		#socket = urllib.request.urlopen(url)
		#socket = urllib.request.urlopen(url,headers={'Connection': 'Keep-Alive',	'Accept': 'text/html, application/xhtml+xml, */*',	'Accept-Language':'zh-CN,zh;q=0.8',	'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'})
		#req=urllib.request.Request(url+'a',headers={'Connection': 'Keep-Alive',	'Accept': 'text/html, application/xhtml+xml, */*',	'Accept-Language':'zh-CN,zh;q=0.8',	'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'})

		req = urllib.request.Request(
				url,
				data=None,
				headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
			)
		socket = urllib.request.urlopen(req)
		#print(f.read().decode('utf-8'))

	except Exception as e:
		print(e)
		return
	xd = pd.ExcelFile(socket)
	df = xd.parse(xd.sheet_names[-1], header=None)
	df = df.drop(0)
	df.columns = ['time','price','change','volume','amount','type']
	df1 = pd.DataFrame(df['time'].tolist(),columns=['time'])
	df1['price'] = df['price'].tolist()
	df1['change'] = df['change'].tolist()
	df1['volume'] = df['volume'].tolist()
	df1['amount'] = df['amount'].tolist()
	df1['type'] = df['type'].tolist()

	df1 = df1[df1['volume'] != 0]
	df1 = df1[df1['amount'] != 0]
	df1 = df1.sort_values('time',ascending = True)
	df1 = df1.reset_index()
	del df1['index']
	return df1


def get_stick_data(code,date = ''):
	if date == '':
		date = dt.datetime.now().strftime('%Y-%m-%d')
	if code[0:1]=='6':
		code ='sh' + code
	else:
		code ='sz' + code

	url = "http://market.finance.sina.com.cn/downxls.php?date=%s&symbol=%s" % (date,code)
	try:
		df = pd.read_csv(url,sep='\t',skiprows=(1),header=None,encoding='latin')
	except Exception as e:
		print(e)
		return

	if df.ix[0].str.contains('alert').ix[0]:
		print('当天没有数据')
		return

	df.columns = ['time','price','change','volume','amount','type']
	df1 = pd.DataFrame(df['time'].tolist(),columns=['time'])
	df1['price'] = df['price'].tolist()
	df1['change'] = df['change'].tolist()
	df1['volume'] = df['volume'].tolist()
	df1['amount'] = df['amount'].tolist()
	df1['type'] = 0
	#del df1['type']
	df1 = df1[df1['volume'] != 0]
	df1 = df1[df1['amount'] != 0]
	df1 = df1.sort_values('time',ascending = True)
	df1 = df1.reset_index()
	del df1['index']
	return df1

def get_qqtick_data(code,date = ''):
	if date == '':
		date = dt.datetime.now().strftime('%Y-%m-%d')
	if code[0:1]=='6':
		code ='sh' + code
	else:
		code ='sz' + code

	date = date.replace('-','')
	url = "http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c=%s&d=%s" % (code,date)

	try:
		df = pd.read_csv(url,sep='\t',skiprows=(1),header=None,encoding='latin')
	except Exception as e:
		print(e)
		return
	df.columns = ['time','price','change','volume','amount','type']
	df1 = pd.DataFrame(df['time'].tolist(),columns=['time'])
	df1['price'] = df['price'].tolist()
	df1['change'] = df['change'].tolist()
	df1['volume'] = df['volume'].tolist()
	df1['amount'] = df['amount'].tolist()
	df1['type'] = 0
	df1 = df1[df1['volume'] != 0]
	df1 = df1[df1['amount'] != 0]
	df1 = df1.sort_values('time',ascending = True)
	df1 = df1.reset_index()
	del df1['index']
	return df1



def get_tick(code,date = ''):
	if date == '':
		date = dt.datetime.now().strftime('%Y-%m-%d')
	try:
		df = ts.get_tick_data(code,date)
	except Exception as e:
		df = None
	if type(df) == pd.core.frame.DataFrame:
		df = df.dropna()
		if len(df) != 0:
			df = df[df['volume'] != 0]
			df = df[df['amount'] != 0]
			df = df.sort_values('time',ascending = True)
			df = df.reset_index()
			del df['index']
			return df

	#print('stick')
	df = get_stick_data(code,date)
	if type(df) == pd.core.frame.DataFrame:
		df = df.dropna()
		if len(df) != 0:
			df = df[df['volume'] != 0]
			df = df[df['amount'] != 0]
			df = df.sort_values('time',ascending = True)
			df = df.reset_index()
			del df['index']
			return df

	#print('qqtick')
	df = get_qqtick_data(code,date)
	if type(df) == pd.core.frame.DataFrame:
		df = df.dropna()
		if len(df) != 0:
			df = df[df['volume'] != 0]
			df = df[df['amount'] != 0]
			df = df.sort_values('time',ascending = True)
			df = df.reset_index()
			del df['index']
			return df

	if date == dt.datetime.now().strftime('%Y-%m-%d'):
		#print('today ticks data')
		df = ts.get_today_ticks(code)
		if type(df) == pd.core.frame.DataFrame:
			df = df.dropna()
			if len(df) != 0:
				df = df[df['volume'] != 0]
				df = df[df['amount'] != 0]
				df = df.sort_values('time',ascending = True)
				df = df.reset_index()
				del df['index']
				return df

	#print('etick')
	df = get_etick_data(code,date)
	if type(df) == pd.core.frame.DataFrame:
		df = df.dropna()
		if len(df) != 0:
			df = df[df['volume'] != 0]
			df = df[df['amount'] != 0]
			df = df.sort_values('time',ascending = True)
			df = df.reset_index()
			del df['index']
			return df

	return 0

if __name__ == '__main__':
	pass
	"""code = '002508'
	date = '2016-10-25'
	print(dt.datetime.now())
	df = get_tick(code,date)
	print(dt.datetime.now())
	if type(df) == pd.core.frame.DataFrame:
		cost = 20
		whole = 1e9
		#res = df_eam(df,cost,whole)
		#print(len(res))"""