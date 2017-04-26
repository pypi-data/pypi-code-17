from .mis import *
import pandas as pd
import datetime as dt
import warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)

def ex_cal(df):
	df = df.sort_values('date',ascending = False)
	print(df)
	ex = []

	flag=0
	x=[]
	y=[]
	ex.append((str(df.iloc[0]['date'])[:10],float(df.iloc[0]['open']),float(df.iloc[0]['high']),float(df.iloc[0]['low']),float(df.iloc[0]['close']),float(df.iloc[0]['volume']),float(df.iloc[0]['p_change']),))

	for i in range(len(df)-1):
		if df.iloc[i]['qclose'] == df.iloc[i+1]['close'] and flag == 0:
			ex.append((str(df.iloc[i+1]['date'])[:10],float(df.iloc[i+1]['open']),float(df.iloc[i+1]['high']),float(df.iloc[i+1]['low']),float(df.iloc[i+1]['close']),float(df.iloc[i+1]['volume']),float(df.iloc[i+1]['p_change']),))

		if df.iloc[i]['qclose'] == df.iloc[i+1]['close'] and flag == 1:
			tmp_o = float(df.iloc[i+1]['open'])
			for j in range(len(x))[::-1]:
				tmp_o = (tmp_o - x[j]) / y[j]
			tmp_o = round(tmp_o,2)

			tmp_h = float(df.iloc[i+1]['high'])
			for j in range(len(x))[::-1]:
				tmp_h = (tmp_h - x[j]) / y[j]
			tmp_h = round(tmp_h,2)

			tmp_l = float(df.iloc[i+1]['low'])
			for j in range(len(x))[::-1]:
				tmp_l = (tmp_l - x[j]) / y[j]
			tmp_l = round(tmp_l,2)

			tmp_c = float(df.iloc[i+1]['close'])
			for j in range(len(x))[::-1]:
				tmp_c = (tmp_c - x[j]) / y[j]
			tmp_c = round(tmp_c,2)

			ex.append((str(df.iloc[i+1]['date'])[:10],tmp_o,tmp_h,tmp_l,tmp_c,float(df.iloc[i+1]['volume']),float(df.iloc[i+1]['p_change'])))

		if df.iloc[i]['qclose'] != df.iloc[i+1]['close']:
			q = float(df.iloc[i]['qclose'])
			c = float(df.iloc[i+1]['close'])
			y1 = (round(float(df.iloc[i]['outstanding'])/float(df.iloc[i]['close']),3)) / (round(float(df.iloc[i+1]['outstanding'])/float(df.iloc[i+1]['close']),3))
			x1 = round((c-q*y1),3)
			y.append(y1)
			x.append(x1)
			print(df.iloc[i]['date'])
			print(x)
			print(y)
			tmp_o = float(df.iloc[i+1]['open'])
			for j in range(len(x))[::-1]:
				tmp_o = (tmp_o - x[j]) / y[j]
				print(x[j],y[j])
			tmp_o = round(tmp_o,2)

			tmp_h = float(df.iloc[i+1]['high'])
			for j in range(len(x))[::-1]:
				tmp_h = (tmp_h - x[j]) / y[j]
			tmp_h = round(tmp_h,2)

			tmp_l = float(df.iloc[i+1]['low'])
			for j in range(len(x))[::-1]:
				tmp_l = (tmp_l - x[j]) / y[j]
			tmp_l = round(tmp_l,2)

			tmp_c = float(df.iloc[i+1]['close'])
			for j in range(len(x))[::-1]:
				tmp_c = (tmp_c - x[j]) / y[j]
			tmp_c = round(tmp_c,2)

			ex.append((str(df.iloc[i+1]['date'])[:10],tmp_o,tmp_h,tmp_l,tmp_c,float(df.iloc[i+1]['volume']),float(df.iloc[i+1]['p_change'])))
			flag=1

	col = ['date','open','high','low','close','volume','p_change']
	df = pd.DataFrame(ex,columns = col)
	df = df.sort_values(by = 'date',ascending=True)

	df.index = df['date']
	df.index = pd.to_datetime(df.index)
	df.index.names = ['date']

	return df


def ex_cal2(df):
	df = df.sort_values('date',ascending = False)
	xx = pd.DataFrame(df[['qclose','close','outstanding',]].shift(1),columns=['qclose','close','outstanding',])
	xx = xx[1:]
	df0 = df[1:]
	xx['date'] = df0['date']
	dfp = df0[df0['close']!=xx['qclose']].head(1)
	if len(dfp) == 0:
		return df
	df0 = df0[df0.date <= dfp.iloc[0].date]
	xx = xx[xx.date <= dfp.iloc[0].date]
	y1 = round(float(xx.iloc[0]['outstanding']) / float(xx.iloc[0]['close'])) / \
		round(float(df0.iloc[0]['outstanding']) / float(df0.iloc[0]['close']))

	y1 = round(y1,4)
	x1 = float(df0.iloc[0]['close']) - float(xx.iloc[0]['qclose']) * y1
	df0[['open','high','low','close']] = ( df0[['open','high','low','close']].astype(float) - x1 ) / y1
	df0['volume'] = df0['volume'].astype(float) * y1

	df = pd.concat([df[df.date > dfp.iloc[0].date],df0])
	df[['open','high','low','close','p_change']] = df[['open','high','low','close','p_change']].round(2)
	df['volume'] = df['volume'].astype(int)

	#df = df.sort_values('date')
	return df

def ex_cal3(df,dfm):
	df = df.sort_values('date',ascending = False)
	try:
		dfm = dfm.sort_values('time',ascending = False)
	except Exception as e:
		dfm = dfm.sort_values('date',ascending = False)

	xx = pd.DataFrame(df[['qclose','close','outstanding',]].shift(1),columns=['qclose','close','outstanding',])
	xx = xx[1:]
	df0 = df[1:]
	xx['date'] = df0['date']
	dfp = df0[df0['close'] != xx['qclose']]
	if len(dfp) == 0:
		df['vwap'] = df['amount'].astype(float) / df['volume'].astype(float)
		dfm['vwap'] = dfm['amount'].astype(float) / (dfm['volume'].astype(float) * 1e2)
		dfm = dfm.reset_index()
		del dfm['index']
		return df,dfm
	#print(dfp)
	coe = []
	for i in range(len(dfp)):
		df0i = df0[df0['date'] == dfp.iloc[i]['date']]
		xxi = xx[xx['date'] == dfp.iloc[i]['date']]
		y1 = round(float(xxi.iloc[0]['outstanding']) / float(xxi.iloc[0]['close'])) / \
			round(float(df0i.iloc[0]['outstanding']) / float(df0i.iloc[0]['close']))
		x1 = float(df0i.iloc[0]['close']) - float(xxi.iloc[0]['qclose']) * y1
		coe.append((dfp.iloc[i]['date'],round(x1,3),y1))
	coe = pd.DataFrame(coe,columns=['date','x','y'])
	coe = coe.sort_values('date')

	#print(coe)
	dres = pd.DataFrame()
	dresm = pd.DataFrame()
	for i in range(len(coe)):
		dfi = df[df['date'] <= dfp.iloc[-i-1]['date']]
		try:
			dfim = dfm[dfm['time'] <= dfp.iloc[-i-1]['date']]
		except Exception as e:
			dfim = dfm[dfm['date'] <= dfp.iloc[-i-1]['date']]

		for j in range(i,len(coe)):
			dfi[['open','high','low','close']] = ( dfi[['open','high','low','close']].astype(float) - coe.iloc[j]['x'] ) / coe.iloc[j]['y']
			dfi[['volume']] = dfi[['volume']].astype(float) * coe.iloc[j]['y']
			dfim[['open','high','low','close']] = ( dfim[['open','high','low','close']].astype(float) - coe.iloc[j]['x'] ) / coe.iloc[j]['y']
			dfim[['volume']] = dfim[['volume']].astype(float) * coe.iloc[j]['y']
		dfi[['open','high','low','close','p_change']] = dfi[['open','high','low','close','p_change']].round(2)
		dfi[['volume']] = dfi[['volume']].astype(int)
		dres = dres.append(dfi)
		df = df[df['date'] > dfp.iloc[-i-1]['date']]

		dfim[['open','high','low','close',]] = dfim[['open','high','low','close',]].round(2)
		dfim[['volume']] = dfim[['volume']].astype(int)
		dresm = dresm.append(dfim)
		try:
			dfm = dfm[dfm['time'] > dfp.iloc[-i-1]['date']]
		except Exception as e:
			dfm = dfm[dfm['date'] > dfp.iloc[-i-1]['date']]

	dres = pd.concat([dres,df])
	dres = dres.sort_values('date',ascending = False)

	dresm = pd.concat([dresm,dfm])
	try:
		dresm = dresm.sort_values('time',ascending = False)
	except Exception as e:
		dresm = dresm.sort_values('date',ascending = False)

	dres['vwap'] = dres['amount'].astype(float) / dres['volume'].astype(float)
	dresm['vwap'] = dresm['amount'].astype(float) / (dresm['volume'].astype(float) * 1e2)

	dresm = dresm.reset_index()
	del dresm['index']

	return dres,dresm

def get_hist_from_sql(code,ndays=60,date="",host = ''):
	if date == "":
		strq = """SELECT date,open,high,low,close,qclose,outstanding,volume,p_change,amount
		FROM %s_hist ORDER BY date DESC LIMIT 0,%s;""" % (code,ndays)
		df = sql_to_df('hist',strq,host = host)
		return df
	else:
		strq = """SELECT date,open,high,low,close,qclose,outstanding,volume,p_change,amount
		FROM %s_hist WHERE date <='%s' ORDER BY date DESC LIMIT 0,%s;""" % (code,date,ndays)
		df = sql_to_df('hist',strq,host = host)
		return df

def ma_cal(dfh):
	name = list((map(str,list(range(1,51)))))
	name = pd.DataFrame(name,columns=['name'])
	name = 'ma' + name
	name = name['name'].tolist()
	df = pd.DataFrame()
	for i in range(5):
		res = []
		for j in range(i,50+i):
			res.append(dfh[i:i+j+1]['close'].astype(float).mean())
		res = pd.DataFrame(res).T
		res.columns = name
		df = df.append(res)
	df['date'] = dfh.iloc[0]['date']
	df.index = range(1,5+1)
	return df

def get_code_list_from_sql(database,num=0,host = ''):
	strq = "SHOW TABLES;"
	df = sql_to_df(database,strq,host = host)
	df = df["Tables_in_" + database].str.replace("_" + database,"")
	df = pd.DataFrame(df)
	if num == 0:
		return df
	else:
		return df[:num]


def get_code_list_hist(dfh,ndays = 100):
	dfh_all = pd.DataFrame()
	for i in range(len(dfh)):
		code = dfh.iloc[i]['Tables_in_hist']
		df = get_hist_from_sql(code,ndays)
		df = ex_cal2(df)
		df['code'] = code
		dfh_all = dfh_all.append(df)
	return dfh_all

def get_ma_hist(num,ndays = 100,database = "hist"):
	dfh = get_code_list_from_sql(database,num)
	res = pd.DataFrame()
	if num == 0:
		num = len(dfh)
	for i in range(num):
		code = dfh.iloc[i]['Tables_in_' + database]
		df = get_hist_from_sql(code,ndays)
		df = ex_cal2(df)

		dfm = ma_cal(df)
		dfm['code'] = code
		res = res.append(dfm)
		print(i)
	return res

def cal_ma_now(df,dft):
	df1 = df[df.index == 1]
	df1 = df1.sort_values(by=['code'],ascending = True)

	dft = dft[dft['volume'] > 0]
	dft = dft.drop_duplicates(['code'], keep='last')
	dft.index = dft['code']
	dft = dft.sort_values(by=['code'],ascending = True)

	df = df[df['code'].isin(dft['code'])]
	df1 = df1[df1['code'].isin(dft['code'])]
	dft = dft[dft['code'].isin(df1['code'])]

	df1.index = range(len(df1))
	df_head = pd.DataFrame([0] * len(df1),columns=['ma0'])
	df1 = pd.concat([df_head.T,df1.T])

	dfi = pd.DataFrame(list(range(1,len(df1)+1)),columns = ['i'],index = df1.index)

	xx = pd.DataFrame(dft['trade'])
	xx.index = range(len(xx))
	xx = pd.concat([xx.T]*(len(df1)-2))
	xx.index = df1.head(len(df1)-2).index

	yy = xx[xx.columns].divide(dfi.head(len(df1)-2)['i'], axis="index")
	yy = df1[df1.columns].head(len(df1)-2).add(yy, axis="index")
	zz = df1[df1.columns].head(len(df1)-2).divide(dfi.head(len(df1)-2)['i'], axis="index")
	res = yy[yy.columns].subtract(zz, axis="index")
	res = (res.shift(1)).drop(['ma0'])
	res = pd.concat([res,df1.tail(2)]).T
	res.index = [0] * len(res)

	dft0 = dft
	dft0.index = [0] * len(dft0)
	res[['trade','open','high','low',]] = dft[['trade','open','high','low',]]

	dftt = pd.DataFrame()
	for i in range(5):
		df0 = df[df.index == i]
		dft0.index = [i] * len(dft0)
		df0[['trade','open','high','low',]] = dft0[['trade','open','high','low',]]
		dftt = pd.concat([dftt,df0])

	return dftt,res

def is_manzu0(df):
	res = pd.DataFrame()
	for i in range(5):
		df0 = df[df.index == i]
		df0['d1'] = df0['ma5'] / df0['ma10'] - 1.0
		df0['d2'] = df0['ma10'] / df0['ma20'] - 1.0
		df0['d3'] = df0['ma20'] / df0['ma30'] - 1.0
		if i == 0:
			df0 = df0[df0['ma5'] < df0['ma10']]
		else:
			df0 = df0[df0['ma5'] > df0['ma10']]

		df0 = df0[df0['ma10'] > df0['ma20']]
		df0 = df0[df0['ma20'] > df0['ma30']]
		if i == 0:
			res = df0
		else:
			res = res[res['code'].isin(df0['code'])]
			df0 = df0[df0['code'].isin(res['code'])]
			res = res.append(df0)
	#print(res)
	df0 = res[res.index == 0]
	df0.index = [0] * len(df0)
	df1 = res[res.index == 1]
	df1.index = [0] * len(df1)
	df2 = res[res.index == 2]
	df2.index = [0] * len(df2)
	df3 = res[res.index == 3]
	df3.index = [0] * len(df3)
	df4 = res[res.index == 4]
	df4.index = [0] * len(df4)

	df0['d1_01'] = df0['d1'] - df1['d1']
	df0['d1_12'] = df1['d1'] - df2['d1']
	df0['d1_23'] = df2['d1'] - df3['d1']
	df0['d1_34'] = df3['d1'] - df4['d1']

	df0['d2_01'] = df0['d2'] - df1['d2']
	df0['d2_12'] = df1['d2'] - df2['d2']
	df0['d2_23'] = df2['d2'] - df3['d2']
	df0['d2_34'] = df3['d2'] - df4['d2']

	df0['d3_01'] = df0['d3'] - df1['d3']
	df0['d3_12'] = df1['d3'] - df2['d3']
	df0['d3_23'] = df2['d3'] - df3['d3']
	df0['d3_34'] = df3['d3'] - df4['d3']

	df0.sort_values(by = ['d1'],ascending = True)
	return df0

#pd.options.display.max_rows = 99
#code = '002508'
#ndays = 100
#date1 = '2016-06-01'
#df = get_hist_from_sql(code,ndays,date1)
#df = get_hist_from_sql(code)
#df = ex_cal(df)
#df = ma_cal(df)

#code='002508'
#df = get_hist_from_sql(code)
#df = ex_cal2(df)

if __name__ == '__main__':
	df = get_code_list_from_sql('hist',num = 20)
	df = get_code_list_hist(df,ndays = 100)

	dd =pd.DataFrame(df['date'].astype(str).unique().tolist(),columns = ['date'])
	dd = dd.sort_values(by = 'date',ascending = True)

	t1 = dt.datetime.now()

	ii = 0
	for d in dd['date'].tolist()[60:len(dd)-10]:
		ii += 1
		print(ii)
		xx = df[df['date'] <= d]
		xx = pd.pivot_table(xx, index=['code','date'],)

		res = pd.DataFrame()
		for code in xx.index.get_level_values('code').unique().tolist():
			dfx = xx.iloc[xx.index.get_level_values('code') == code]
			dfx.index = dfx.index.droplevel(0)
			dfx['date'] = dfx.index
			dfx = dfx.sort_values(by='date',ascending=False)
			dfx.index = range(len(dfx))
			dfm = ma_cal(dfx)
			dfm['code'] = code
			res = res.append(dfm)
		# deal res...
	print(dt.datetime.now()-t1)

	"""df = get_ma_hist(num = 100)
	while True:
		dft0 = ts.get_today_all()
		dft0 = dft0[dft0['turnoverratio']>3]
		dft0 = dft0[dft0['turnoverratio']<15]
		dft,res = cal_ma_now(df,dft0)
		dfn = dft.append(res)
		df2 = is_manzu0(dfn)
		if len(df2) > 5:
			print(df2.head(5).code)
		else:
			print(df2.code)"""