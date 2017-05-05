# -*- coding: gb2312 -*-
"""
Created on Fri Aug 19 09:03:14 2016

@author: lby
"""
import time
import pymysql
import tushare as ts
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.pool import QueuePool

def sql_to_df(database,strq,host=""):
	if host == "":
		str_con = "mysql+pymysql://root:523240@localhost/%s?charset=utf8" % database
	else:
		str_con = "mysql+pymysql://root:523240@%s/%s?charset=utf8" % (host,database)
	#print ("VM: %.2fMb" % ((float(psutil.Process().memory_info_ex().vms) / 1024.0) / 1024.0))
	engine = create_engine(str_con)
	#engine = create_engine(str_con, pool_recycle=1)
	#engine = create_engine(str_con, pool_size=1, max_overflow=0)
	#engine = create_engine(str_con, poolclass=NullPool)
	#engine = create_engine(str_con, poolclass=QueuePool)

	while True:
		try:
			con = engine.connect()
			break
		except Exception as e:
			time.sleep(5)
			continue

	try:
		res = con.execute(strq)
	except Exception as e:
		print(e)
		con.invalidate()
		con.close()
		engine.dispose()
		return

	df = pd.DataFrame(res.fetchall(),columns = res.keys())
	con.invalidate()
	con.close()
	engine.dispose()
	return df

def df_to_sql(database,table,df,option = 'append',host=""):
	if host == "":
		str_con = "mysql+pymysql://root:523240@localhost/%s?charset=utf8" % database
	else:
		str_con = "mysql+pymysql://root:523240@%s/%s?charset=utf8" % (host,database)

	#str_con = "mysql+pymysql://root:523240@localhost/%s?charset=utf8" % database
	engine = create_engine(str_con)
	#engine = create_engine(str_con, pool_recycle=1)
	#engine = create_engine(str_con, poolclass=NullPool)
	#engine = create_engine(str_con, poolclass=QueuePool)
	#engine = create_engine(str_con, pool_size=1, max_overflow=0)
	try:
		df.to_sql(table,engine,if_exists=option)
	except Exception as e:
		print(e)
	engine.dispose()

def sql_modify(database,strq,host1=""):
	if host1 == "":
		con = pymysql.connect(host='localhost',user='root',passwd='523240',db=database,charset='utf8')
	else:
		con = pymysql.connect(host=host1,user='root',passwd='523240',db=database,charset='utf8')

	#con = pymysql.connect(host='localhost',user='root',passwd='523240',db=database,charset='utf8')
	cur = con.cursor()
	try:
		cur.execute(strq)
	except Exception as e:
		print(e)
	try:
		con.commit()
	except Exception as e:
		print(e)
	cur.close()
	con.close()

def while_get_today_all():
	while True:
		try:
			df = ts.get_today_all()
			return df
		except Exception as e:
			print(e)
			time.sleep(.1)
			continue

def while_get_tick_data(cd,da):
	while True:
		try:
			df = ts.get_tick_data(cd,date=da)
			return df
		except Exception as e:
			print(e)
			time.sleep(.1)
			continue

def while_get_today_ticks(cd):
	for i in range(5):
		try:
			df = ts.get_today_ticks(cd)
			return df
		except Exception as e:
			print(e)
			time.sleep(.1)
			continue
