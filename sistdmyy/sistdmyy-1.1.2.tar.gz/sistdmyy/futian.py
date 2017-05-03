
from sqlalchemy import create_engine
from sqlalchemy import types
import re
import pymssql
import numpy as np
import pandas as pd
import re
import os
import xlrd
import openpyxl
import time
from functools import reduce
import datetime
import calendar
from sistdmyy import *
#数据库访问控制

_m=db()
db_query=_m.frommssql


qh={'盐田区':'440308','宝安区':'440306','罗湖区':'440303','福田区':'440304','龙岗区':'440307','南山区':'440305',
'光明新区':'440309','坪山新区':'440310','龙华新区':'440342'}




def test():
    clrq='2017-04-20'
    sql="""
        select top 10  '%%'+jgmc from basedb.dbo.t_zzjgjz where clrq>='%s'
        """%clrq
    df=db_query(sql)
    return df
#------------------------------------------------------------1、专业服务机构----------------------------------------------------------------------------------
def getdf_fuwu(startdate,enddate,xzqh):
     xzqh=qh[xzqh]
     sql="""
        select jgmc as '机构名称',jglx as '机构类型', 
        fddbr as '法定代表人人',jgdhhm as '固定电话',jgmobile as '移动电话', 
        jgdz as '机构地址', 
        convert(varchar(100),clrq,23) as '成立日期',zczj_rmb as '注册资金',zgrs as '职工人数', 
        jyfw as  '机构简介', 
        a.jjhy as '所属行业',a.jjhydm , 
        case substring(a.jjhydm,2,3) when  '723' then '咨询与调查'  when '722' then '法律服务' when '721' 
        then '企业管理服务' when '729' then '其他商务服务' when '725' then '知识产权服务' when '752' then '科技中介服务'  else '文化艺术经纪代理' end as '新行业类别' 
        from BaseDB.dbo.t_zzjgjz a 
        where 
        clrq>='%s' and clrq<'%s' 
        and  XZQHdm='%s'  
        and substring(a.jjhydm,2,3) in('723','722','721','729','725','752','894') 
        and jglxdm in('1','2')
        """%(startdate,enddate,xzqh)
     df=db_query(sql)
     return df


#------------------------------------------------------------2、新增大型企业----------------------------------------------------------------------------------

def getdf_xz(startdate,enddate,xzqh):
     xzqh=qh[xzqh]
     #此处sql,得到
     sql="""
        select rtrim(ltrim(entid)) as entid,shname,rank() over (partition by entid order by capprop desc) as rn,fddbr from( 
        select a.*,b.fddbr from BaseDB.dbo.T_ZZJGJZ b,( 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s' )
        and  shatt=1 and entstatuscode=0) a  
        where a.shid=b.ztsfdm 
        union 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt,9,2))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop,shname as fddbr 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s') 
        and  shatt =0  and entstatuscode=0 
        UNION 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop, 
        case when len(shname)>4 then '外地企业法人未知' else shname end as fddbr 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s') 
        and  shatt =2  and entstatuscode=0) aa where aa.shname is not null and aa.fddbr is not null
        """%(startdate,enddate,startdate,enddate,startdate,enddate)

     sql0="""
        select xx1.jjhy as '行业大类',xx.* from
        (select ztsfdm as entid,jyfw as '项目简介',xzqh as '落户区',jglxdm as 机构类型,jgmc as '注册公司名称',
        convert(varchar(100),clrq,23) as '注册日期', qylx as '公司性质', 
        zgrs as '职工人数', zczj as '注册资金',hbzl as '货币种类' ,zczj_rmb as '注册资金_人民币' , 
        jjhydm as '经济行业代码', jjhy as '经济行业小类','' as '投资国别', 
        jgdz as '机构地址', 
        case when qylxdm like '[567w]%%' then '外资' else '内资' end as '内外资' 
        from basedb.dbo.t_zzjgjz where xzqhdm='%s' and jglxdm in('1','2','B') 
        and clrq>='%s' and clrq<'%s' ) xx 
        left join  
        (select jjhydm,jjhy from basedb.dbo.dict_jjhy) xx1 
        on substring(xx.[经济行业代码],1,1)=xx1.jjhydm
        """%(xzqh,startdate,enddate)
     sql1="select entid ,shname as '主要投资方',fddbr as '主要投资方法人(联系人)'  from(%s) t where rn=1 "%(sql)
     sql2="select entid ,shname as '次要合伙投资方' from(%s) t where rn>1 "%(sql)
     sql3="select * from (%s) tt "%sql0
     df1,df2=db_query(sql1),db_query(sql2)

     df1=df1.groupby('entid').agg({'主要投资方':lambda x: ','.join(map(lambda i:'' if i is None else i,x)),'主要投资方法人(联系人)':lambda x:','.join(map(lambda i:'' if i is None else i,x))})
     df1['entid']=df1.index
     df1.index=range(len(df1))

     df2=df2.groupby('entid').agg({'次要合伙投资方':lambda x:','.join(map(lambda i:'' if i is None else i,x))})
     df2['entid']=df2.index
     df2.index=range(len(df2))

     df3=pd.merge(df1,df2,on='entid',how='left') #主要投资人
     #df2=db_query(sql2)
     df=db_query(sql3)#内资
     dfx=pd.merge(df3,df,on='entid',how='right')
     dfx['外资项目新增注册资金（万美元）']=''
     dfx['内资项目新增注册资金（万元人民币）']=''
     dfx['项目投资总额（亿人民币）']=dfx['注册资金_人民币']/10000
     dx=['主要投资方','次要合伙投资方','主要投资方法人(联系人)','项目投资总额（亿人民币）','行业大类','项目简介',
        '落户区','注册公司名称','注册日期','公司性质','外资项目新增注册资金（万美元）','内资项目新增注册资金（万元人民币）', 
        '职工人数','注册资金','货币种类','注册资金_人民币','经济行业代码','经济行业小类','投资国别','机构地址','内外资','机构类型']

     dfx=shift(dfx,dx)
     dfx=dfx.drop_duplicates()
     dfx['机构类型']=dfx[['机构类型']].applymap(lambda x: '企业' if x in['1','2'] else '个体户')
     return dfx



#后缀Z给其它主题用（产业信息)
def getdf_xzz(startdate,enddate,xzqh):
     xzqh=qh[xzqh]
     sql="""
        select rtrim(ltrim(entid)) as entid,shname,rank() over (partition by entid order by capprop desc) as rn,fddbr from( 
        select a.*,b.fddbr from BaseDB.dbo.T_ZZJGJZ b,( 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s' )
        and  shatt=1 and entstatuscode=0) a 
        where a.shid=b.ztsfdm 
        union 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt,9,2))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop,shname as fddbr 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s') 
        and  shatt =0  and entstatuscode=0 
        UNION 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop, 
        case when len(shname)>4 then '外地企业法人未知' else shname end as fddbr 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s') 
        and  shatt =2  and entstatuscode=0) aa where aa.shname is not null and aa.fddbr is not null
        """%(startdate,enddate,startdate,enddate,startdate,enddate)
    
     sql0="""
         select xx1.jjhy as '行业大类',xx.* from
         (select ztsfdm as entid,jyfw as '项目简介',xzqh as '落户区',jglxdm as 机构类型,jgmc as '注册公司名称',convert(varchar(100),clrq,23) as '注册日期', qylx as '公司性质', 
        zgrs as '职工人数', zczj as '注册资金',hbzl as '货币种类' ,zczj_rmb as '注册资金_人民币' , jjhydm as '经济行业代码', jjhy as '经济行业小类','' as '投资国别', 
        jgdz as '机构地址', case when qylxdm like '[567w]%%' then '外资' else '内资' end as '内外资' from basedb.dbo.t_zzjgjz where xzqhdm='%s' and jglxdm in('1','2','B') 
        and clrq>='%s' and clrq<'%s' ) xx left join  
        (select jjhydm,jjhy from basedb.dbo.dict_jjhy) xx1 on substring(xx.[经济行业代码],1,1)=xx1.jjhydm
        """%(xzqh,startdate,enddate)
     df=db_query(sql0)
     df['机构类型']=df[['机构类型']].applymap(lambda x: '企业' if x in['1','2'] else '个体户')

     df=df.drop_duplicates()
     return df

def getdf_daxing_nei(startdate,enddate,xzqh):
     xzqh=qh[xzqh]
     sql="""
        select rtrim(ltrim(entid)) as entid,shname,rank() over (partition by entid order by capprop desc) as rn,fddbr from( 
        select a.*,b.fddbr from BaseDB.dbo.T_ZZJGJZ b,( 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s' )
        and  shatt=1 and entstatuscode=0) a 
        where a.shid=b.ztsfdm 
        union 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt,9,2))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop,shname as fddbr 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s') 
        and  shatt =0  and entstatuscode=0 
        UNION 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop, 
        case when len(shname)>4 then '外地企业法人未知' else shname end as fddbr 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s') 
        and  shatt =2  and entstatuscode=0) aa where aa.shname is not null and aa.fddbr is not null
        """%(startdate,enddate,startdate,enddate,startdate,enddate)
    
     sql0="""
        select xx1.jjhy as '行业大类',xx.* from
        (select ztsfdm as entid,jyfw as '项目简介',xzqh as '落户区',jgmc as '注册公司名称',convert(varchar(100),clrq,23) as '注册日期', qylx as '公司性质', 
        zgrs as '职工人数', zczj as '注册资金',hbzl as '货币种类' ,zczj_rmb as '注册资金_人民币' , jjhydm as '经济行业代码', jjhy as '经济行业小类','' as '投资国别', 
        jgdz as '机构地址', case when qylxdm like '[567w]%%' then '外资' else '内资' end as '内外资' from basedb.dbo.t_zzjgjz where xzqhdm='%s' and zczj_rmb>=10000  and jglxdm in('1','2') 
        and clrq>='%s' and clrq<'%s' ) xx left join 
        (select jjhydm,jjhy from basedb.dbo.dict_jjhy) xx1 on substring(xx.[经济行业代码],1,1)=xx1.jjhydm
        """%(xzqh,startdate,enddate)
     sql1="""select entid ,shname as '主要投资方',fddbr as '主要投资方法人(联系人)'  from(%s) t where rn=1 """%(sql)
     sql2="""select entid ,shname as '次要合伙投资方' from(%s) t where rn>1 """%(sql)
     sql3="""select * from (%s) tt where tt.[内外资]='内资'"""%sql0
     df1,df2=db_query(sql1),db_query(sql2)
     df1=df1.groupby('entid').agg({'主要投资方':lambda x: ','.join(map(lambda i:'' if i is None else i,x)),'主要投资方法人(联系人)':lambda x:','.join(map(lambda i:'' if i is None else i,x))})
     df1['entid']=df1.index
     df1.index=range(len(df1))
     df2=df2.groupby('entid').agg({'次要合伙投资方':lambda x:','.join(map(lambda i:'' if i is None else i,x))})
     df2['entid']=df2.index
     df2.index=range(len(df2))
     df3=pd.merge(df1,df2,on='entid',how='left') #主要投资人
     #df2=db_query(sql2)
     df=db_query(sql3)#内资
     dfx=pd.merge(df3,df,on='entid',how='right')
     dfx['外资项目新增注册资金（万美元）']=''
     dfx['内资项目新增注册资金（万元人民币）']=''
     dfx['内资项目投资总额（亿人民币）']=dfx['注册资金_人民币']/10000
     dx=['主要投资方','次要合伙投资方','主要投资方法人(联系人)','内资项目投资总额（亿人民币）','行业大类','项目简介',
        '落户区','注册公司名称','注册日期','公司性质','外资项目新增注册资金（万美元）','内资项目新增注册资金（万元人民币）', 
        '职工人数','注册资金','货币种类','注册资金_人民币','经济行业代码','经济行业小类','投资国别','机构地址','内外资']
     dfx=shift(dfx,dx)
     
     return dfx


def getdf_daxing_neiz(startdate,enddate,xzqh):
     xzqh=qh[xzqh]
     sql="""
        select rtrim(ltrim(entid)) as entid,shname,rank() over (partition by entid order by capprop desc) as rn,fddbr from( 
        select a.*,b.fddbr from BaseDB.dbo.T_ZZJGJZ b,( 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s' )
        and  shatt=1 and entstatuscode=0) a 
        where a.shid=b.ztsfdm 
        union 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt,9,2))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop,shname as fddbr 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s') 
        and  shatt =0  and entstatuscode=0 
        UNION 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop, 
        case when len(shname)>4 then '外地企业法人未知' else shname end as fddbr 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s') 
        and  shatt =2  and entstatuscode=0) aa where aa.shname is not null and aa.fddbr is not null
        """%(startdate,enddate,startdate,enddate,startdate,enddate)
    
     sql0="""
        select xx1.jjhy as '行业大类',xx.* from
        (select ztsfdm as entid,jyfw as '项目简介',xzqh as '落户区',jgmc as '注册公司名称',convert(varchar(100),clrq,23) as '注册日期', qylx as '公司性质', 
        zgrs as '职工人数', zczj as '注册资金',hbzl as '货币种类' ,zczj_rmb as '注册资金_人民币' , jjhydm as '经济行业代码', jjhy as '经济行业小类','' as '投资国别', 
        jgdz as '机构地址', case when qylxdm like '[567w]%%' then '外资' else '内资' end as '内外资' from basedb.dbo.t_zzjgjz where xzqhdm='%s' and zczj_rmb>=10000  and jglxdm in('1','2') 
        and clrq>='%s' and clrq<'%s' ) xx left join 
        (select jjhydm,jjhy from basedb.dbo.dict_jjhy) xx1 on substring(xx.[经济行业代码],1,1)=xx1.jjhydm
        """%(xzqh,startdate,enddate)
     df=db_query(sql0)
     df=df.drop_duplicates()
     return df



def getdf_daxing_wai(startdate,enddate,xzqh):
     xzqh=qh[xzqh]
     sql="""
        select rtrim(ltrim(entid)) as entid,shname,rank() over (partition by entid order by capprop desc) as rn,fddbr from( 
        select a.*,b.fddbr from BaseDB.dbo.T_ZZJGJZ b,( 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s' )
        and  shatt=1 and entstatuscode=0) a 
        where a.shid=b.ztsfdm 
        union 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt,9,2))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop,shname as fddbr 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s') 
        and  shatt =0  and entstatuscode=0 
        UNION 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop, 
        case when len(shname)>4 then '外地企业法人未知' else shname end as fddbr 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s') 
        and  shatt =2  and entstatuscode=0) aa 
        """%(startdate,enddate,startdate,enddate,startdate,enddate)
            
     sql0="""
         select xx1.jjhy as '行业大类',xx.* from
         (select ztsfdm as entid,jyfw as '项目简介',xzqh as '落户区',jgmc as '注册公司名称',convert(varchar(100),clrq,23) as '注册日期', qylx as '公司性质', 
         zgrs as '职工人数', zczj as '注册资金',hbzl as '货币种类' ,zczj_rmb as '注册资金_人民币' , jjhydm as '经济行业代码', jjhy as '经济行业小类','' as '投资国别', 
         jgdz as '机构地址', case when qylxdm like '[567w]%%' then '外资' else '内资' end as '内外资' from basedb.dbo.t_zzjgjz where xzqhdm='%s' and zczj_rmb>=3100 and jglxdm in('1','2') 
         and clrq>='%s' and clrq<'%s' ) xx left join 
         (select jjhydm,jjhy from basedb.dbo.dict_jjhy) xx1 on substring(xx.[经济行业代码],1,1)=xx1.jjhydm
         """%(xzqh,startdate,enddate)
     sql1="""select entid ,shname as '主要投资方',fddbr as '主要投资方法人(联系人)'  from(%s) t where rn=1 """%(sql)
     sql2="""select entid ,shname as '次要合伙投资方' from(%s) t where rn>1 """%(sql)
     sql3="""select * from (%s) tt where tt.[内外资]='外资'"""%sql0
     df1,df2=db_query(sql1),db_query(sql2)
     df1['主要投资方'],df1['主要投资方法人(联系人)']=df1['主要投资方'].fillna(''),df1['主要投资方法人(联系人)'].fillna('')
     df1=df1.groupby('entid').agg({'主要投资方':lambda x: ','.join(map(lambda i:'' if i is None else i,x)),'主要投资方法人(联系人)':lambda x:','.join(map(lambda i:'' if i is None else i,x))})
     df1['entid']=df1.index
     df1.index=range(len(df1))
     df2['次要合伙投资方']=df2['次要合伙投资方'].fillna('')
     df2=df2.groupby('entid').agg({'次要合伙投资方':lambda x:','.join(map(lambda i:'' if i is None else i,x))})
     df2['entid']=df2.index
     df2.index=range(len(df2))
     df3=pd.merge(df1,df2,on='entid',how='left') #主要投资人
     #df2=db_query(sql2)
     df=db_query(sql3)#内资
     dfx=pd.merge(df3,df,on='entid',how='right')
     dfx['外资项目新增注册资金（万美元）']=''
     dfx['内资项目新增注册资金（万元人民币）']=''
     dfx['项目投资总额（亿人民币）']=dfx['注册资金_人民币']/10000
     dx=['主要投资方','次要合伙投资方','主要投资方法人(联系人)','项目投资总额（亿人民币）','行业大类','项目简介',
        '落户区','注册公司名称','注册日期','公司性质','外资项目新增注册资金（万美元）','内资项目新增注册资金（万元人民币）', 
        '职工人数','注册资金','货币种类','注册资金_人民币','经济行业代码','经济行业小类','投资国别','机构地址','内外资']
     dfx=shift(dfx,dx)
     
     return dfx


def getdf_daxing_waiz(startdate,enddate,xzqh):
     xzqh=qh[xzqh]
     sql="""
        select rtrim(ltrim(entid)) as entid,shname,rank() over (partition by entid order by capprop desc) as rn,fddbr from( 
        select a.*,b.fddbr from BaseDB.dbo.T_ZZJGJZ b,( 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s' )
        and  shatt=1 and entstatuscode=0) a 
        where a.shid=b.ztsfdm 
        union 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt,9,2))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop,shname as fddbr 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s') 
        and  shatt =0  and entstatuscode=0 
        UNION 
        select entid,shid,shatt,'{'+shname+'-'+ltrim(str(capamt))+'-'+ltrim(str(capprop,9,2))+'%%}' as shname,capprop, 
        case when len(shname)>4 then '外地企业法人未知' else shname end as fddbr 
        from regdb.dbo.tdsh where entid in(select ztsfdm from BaseDB.dbo.t_zzjgjz where clrq>='%s' and clrq<'%s') 
        and  shatt =2  and entstatuscode=0) aa 
        """%(startdate,enddate,startdate,enddate,startdate,enddate)
    
     sql0="""select xx1.jjhy as '行业大类',xx.* from
         (select ztsfdm as entid,jyfw as '项目简介',xzqh as '落户区',jgmc as '注册公司名称',convert(varchar(100),clrq,23) as '注册日期', qylx as '公司性质', 
        zgrs as '职工人数', zczj as '注册资金',hbzl as '货币种类' ,zczj_rmb as '注册资金_人民币' , jjhydm as '经济行业代码', jjhy as '经济行业小类','' as '投资国别', 
        jgdz as '机构地址', case when qylxdm like '[567w]%%' then '外资' else '内资' end as '内外资' from basedb.dbo.t_zzjgjz where xzqhdm='%s' and zczj_rmb>=3100 and jglxdm in('1','2') 
        and clrq>='%s' and clrq<'%s' ) xx left join 
        (select jjhydm,jjhy from basedb.dbo.dict_jjhy) xx1 on substring(xx.[经济行业代码],1,1)=xx1.jjhydm"""%(xzqh,startdate,enddate)
     sql3="""select * from (%s) tt where tt.[内外资]='外资'"""%sql0
     df=db_query(sql3)
     df=df.drop_duplicates()
     return df


#--------------------------------------------------------------3 迁移--------------------------------------------------------------------------------------
def getdf_nei(startdate,enddate,xzqh):
     #startdate='2016-09-01'
     #enddate='2016-10-01'
     #xzqh='福田区'
     dz=xzqh[:-1]
     sql0="""
        select entid from regdb.dbo.tdalteritem where alteritemcode in('02','04','10')  
        and alterdate>='%s' and alterdate<'%s'
        """%(startdate,enddate)
     sql=""" 
        select entid,addr,authdate,rnx 
        from( 
        select  
        aa.entid,aa.addr,aa.authdate as authdate ,bb.authdate as authdate1,row_number() over(partition BY 
        aa.entid order by aa.authdate desc) as rnx 
        from RegDB.dbo.tdbase aa , 
        (
        select a.entid,addr,authdate 
        from(
        select entid,addr,authdate from regdb.dbo.tdbase) a , 
        (select * from(select entid,alterdate ,alteritemcode,row_number() over (partition by entid order by alterdate desc) as rn 
         from RegDB.dbo.tdalteritem 
        where  alteritemcode in('02','04','10')  and alterdate>='%s'  
        and alterdate<'%s' ) bx  where rn=1) b 
        where a.entid=b.entid and a.authdate=b.alterdate)  bb 
        where  aa.authdate<=bb.authdate and aa.entid=bb.entid  and aa.authdate<'%s'  
        and aa.entid in(select entid from regdb.dbo.tdalteritem where alteritemcode in('02','04','10') 
        and alterdate>='%s' and alterdate<'%s')) tt 
        where rnx in(1,2) 
        """%(startdate,enddate,enddate,startdate,enddate)
     sql1="""
         select tt1.entid,tt1.addr as  '变更前地址',tt2.addr as '变更后地址',convert(varchar(100),tt2.authdate,23) as '变更日期', 
         case 
         when SUBSTRING(tt1.addr,4,2)!=SUBSTRING(tt2.addr,4,2) and charindex('%s',tt2.addr)>0 then '市内迁入%s区' 
         when SUBSTRING(tt1.addr,4,2)!=SUBSTRING(tt2.addr,4,2) and  charindex('%s',tt1.addr)>0 then '%s区迁出到市内' end  as '迁移状态' 
         from(%s  and rnx=2) tt1,(%s and rnx=1) tt2 where 
          SUBSTRING(tt1.addr,4,2)!=SUBSTRING(tt2.addr,4,2) and ( charindex('%s',tt1.addr)>0 or  charindex('%s',tt2.addr)>0) and tt1.entid=tt2.entid  
          """%(dz,dz,dz,dz,sql,sql,dz,dz)
     sql2="""select EntID ,SHName as '股东名称',CapAmt as '出资额',CapProp as '出资比例' from [CLUSTER2014DB2\MSSQLSERVER2].[regDB].[dbo].[tdSH]  
         where EntID  in(%s) and entstatuscode=0"""%(sql0)
     ##
     sql3="""
        select entid, [股东信息]= '{'+[股东名称]+'-'+'出资额:'+ltrim(str([出资额],10,2))+'(万元)-'+'出资比例:'+ltrim(str([出资比例],9,4))+'%%}'  
        from (%s) t  """%(sql2)
     sql4="""
            select ztsfdm as entid,tydm as '统一社会信用代码',jgdm as '组织机构代码',zch as '注册号', 
            jgmc as '企业名称',zczj_rmb as '注册资金',hbzl as '货币种类',qylx as '企业类型',jjhy as '行业类型' 
            from basedb.dbo.t_zzjgjz where jglxdm in('1','2') and ztsfdm in(%s) 
            """%sql0
     df3=db_query(sql4)
     df1=db_query(sql3)
     dff=df1.groupby('entid').agg({'股东信息':lambda x:','.join(map(lambda i:'' if i is None else i,x))})
     dff['entid']=dff.index
     dff['entid']=dff[['entid']].applymap(lambda x:x.strip())
     dff.index=range(len(dff))
     df2=db_query(sql1)
     df2['entid']=df2[['entid']].applymap(lambda x:x.strip())
     df=pd.merge(df2,dff,on='entid',how='left')
     
     df=pd.merge(df3,df,on='entid')
     a=['统一社会信用代码','组织机构代码','注册号','企业名称','注册资金','货币种类','企业类型','股东信息','核准日期','经济行业','变更前注册地址','变更后注册地址','迁移状态']
     #df=shif(df,a)

     #df['entid']=df[['entid']].applymap(lambda x:'''+x)
     #df['注册号']=df[['注册号']].applymap(lambda x: '''+x)
     #df['组织机构代码']=df[['组织机构代码']].applymap(lambda x:'''+x)
     #df['统一社会信用代码']=df[['统一社会信用代码']].applymap(lambda x:'''+x)
     return df



def getdf_wai(startdate,enddate,xzqh):
     #startdate='2016-10-01'
     #enddate='2016-11-01'
     dz=xzqh[:-1]
     sql1="""select EntID as entid ,EntSCCode as '统一社会信用代码',EntOrgCode as '组织机构代码',EntRegNO as '注册号', 
        EntName as '企业名称',Addr as '注册地址',RegCap as '注册资金',CurrencyCode as '货币种类代码', 
        Currency as '货币种类',EntTypeCode as '企业类型代码',EntType as '企业类型',IndClassCode as '行业分类代码', 
        IndName as '经济行业',
        convert(varchar(100),AuthDate,23) as '核准日期', 
        Memo as '迁移信息', 
        EntStatusCode as '主体记录状态代码', 
        EntStatus as '主体记录状态'  
        from [regDB].[dbo].[tdBase] a 
        left join [regDB].[dbo].tcIndClass abc1 
        on a.IndClassCode =abc1.Code 
        left join [CLUSTER2014DB2\MSSQLSERVER2].[RegDB].[dbo].[tcCurrency] abc2 
        on a.CurrencyCode = abc2.Code 
        left join [CLUSTER2014DB2\MSSQLSERVER2].[RegDB].[dbo].[tcEntType] abc3 
        on a.EntTypeCode = abc3.Code 
        left join [CLUSTER2014DB2\MSSQLSERVER2].[RegDB].[dbo].[tcEntStatus] abc4 
        on a.EntStatusCode = abc4.Code 
        where  
        Addr like '%%%s%%' and SUBSTRING(EntTypeCode,1,1)!='B' and  
        (EntStatusCode=-3 OR  Memo like '%%迁出%%'OR  Memo like '%%迁移至%%') and entstatuscode=0 
        and AuthDate>='%s' and AuthDate<'%s' 
        """%(dz,startdate,enddate)
        #####
     sql2="""select EntID ,SHName as '股东名称',CapAmt as '出资额',CapProp as '出资比例' 
            from [regDB].[dbo].[tdSH]  
            where EntID  in 
            (select EntID  from (%s)tt) 
            and EntStatusCode=0"""%(sql1)
     sql3="""select entid, [股东信息]= '{'+[股东名称]+'-'+'出资额:'+ltrim(str([出资额],10,2))+'(万元)-'+'出资比例:'+ltrim(cast([出资比例] as varchar))+'%%}'  
            from (%s) t """%(sql2)
     df=db_query(sql3)
     df1=df.groupby('entid').agg({'股东信息':lambda x:','.join(map(lambda i:'' if i is None else i,x))})
     df1['entid']=df1.index
     df1.index=range(len(df1))
     df2=db_query(sql1)
     df=df3=pd.merge(df1,df2,on='entid')
     #df['entid']=df[['entid']].applymap(lambda x:'''+x)
     #df['注册号']=df[['注册号']].applymap(lambda x: '''+x)
     #df['组织机构代码']=df[['组织机构代码']].applymap(lambda x:'''+x)
     #df['统一社会信用代码']=df[['统一社会信用代码']].applymap(lambda x:'''+x)

     return df



#-------------------------------------------------------------4 监测---------------------------------------------------------------------------------------

#enddate是最大有效月+1


def getdf_sb(enddate,xzqh):
      #enddate='2016-09-01'
      xzqh=qh[xzqh]
      sql="""
           SELECT zzjgdm as jgdm  
           , min(zjtbn+'-'+zjtby+'-01') t3 
           ,max(zjtbn+'-'+zjtby+'-01') t2
           ,datediff(mm,max(zjtbn+'-'+zjtby+'-01'),'%s')-1 t4 
            FROM sbsj.[RESMG].[GGXY_QYCBXX108635] 
            group by zzjgdm having datediff(mm,max(zjtbn+'-'+zjtby+'-01'),'%s')>1"""%(enddate,enddate)
      sql2="""
            select  ztsfdm,jgdm,jgmc,zczj,hbzl,zczj_rmb,qylx,jjhy from basedb.dbo.t_zzjgjz where ((jgdm in(select jgdm from(%s) tt )) ) 
            and ztztdm>=0 and jglxdm in('1','2')  
            and xzqhdm='%s' and ((qylxdm not like '[567w]%%' and zczj_rmb>=10000) or (qylxdm like '[567w]%%' and zczj_rmb>=3100))
            """%(sql,xzqh)


      sqlx="""
            select ztsfdm,a.jgdm,a.jgmc,zczj,hbzl,zczj_rmb,qylx,jjhy,rq,b.t3,b.t2,b.t4 from
            (select  ztsfdm,jgdm,jgmc,zczj,hbzl,zczj_rmb,qylx,jjhy,convert(varchar(100),clrq,23) as rq from basedb.dbo.t_zzjgjz where  
            ztztdm>=0 and jglxdm in('1','2')  
            and xzqhdm='%s' and ((qylxdm not like '[567w]%%' and zczj_rmb>=10000) or (qylxdm like '[567w]%%' and zczj_rmb>=3100))) a,
            (%s) b where a.jgdm=b.jgdm 
            """%(xzqh,sql)

      sql3="""
            select * from(
            select entid,'{'+shname+'-出资额:'+ltrim(str(capamt,10,4))+'-股份:'+ltrim(str(capprop,9,2))+'%%}'  
            as sh from regdb.dbo.tdsh where entid in(select ztsfdm from (%s) tt)  
            and entstatuscode=0 ) aa where sh is not null
            """%(sql2)

      #社保数据存在当jgdm为空时
      
      sqly1="""
           SELECT qymc as jgmc  
           , min(zjtbn+'-'+zjtby+'-01') t3 
           ,max(zjtbn+'-'+zjtby+'-01') t2
           ,datediff(mm,max(zjtbn+'-'+zjtby+'-01'),'%s')-1 t4 
            FROM sbsj.[RESMG].[GGXY_QYCBXX108635]  where zzjgdm is null 
            group by qymc having datediff(mm,max(zjtbn+'-'+zjtby+'-01'),'%s')>1
            """%(enddate,enddate)
      sqly2="""
            select  ztsfdm,jgdm,jgmc,zczj,hbzl,zczj_rmb,qylx,jjhy from basedb.dbo.t_zzjgjz where ((jgmc in(select jgmc from(%s) tt )) ) 
            and ztztdm>=0 and jglxdm in('1','2')  
            and xzqhdm='%s' and ((qylxdm not like '[567w]%%' and zczj_rmb>=10000) or (qylxdm like '[567w]%%' and zczj_rmb>=3100))
            """%(sqly1,xzqh)


      sqly="""
            select ztsfdm,a.jgdm,a.jgmc,zczj,hbzl,zczj_rmb,qylx,jjhy,rq,b.t3,b.t2,b.t4 from
            (select  ztsfdm,jgdm,jgmc,zczj,hbzl,zczj_rmb,qylx,jjhy,convert(varchar(100),clrq,23) as rq from basedb.dbo.t_zzjgjz where  
            ztztdm>=0 and jglxdm in('1','2')  
            and xzqhdm='%s' and ((qylxdm not like '[567w]%%' and zczj_rmb>=10000) or (qylxdm like '[567w]%%' and zczj_rmb>=3100))) a,
            (%s) b where a.jgmc=b.jgmc
             """%(xzqh,sqly1)


     
      sqly3="""
            select * from(
            select entid,'{'+shname+'-出资额:'+ltrim(str(capamt,10,4))+'-股份:'+ltrim(str(capprop,9,2))+'%%}'  
            as sh from regdb.dbo.tdsh where entid in(select ztsfdm from (%s) tt)  
            and entstatuscode=0 ) aa where sh is not null
            """%(sqly2)

      

      
      df=db_query(sql3)
      dfy=db_query(sqly3)
      df=pd.concat([df,dfy],ignore_index=True)
      df=df.groupby('entid').agg({'sh':lambda x: ','.join(map(lambda i:'' if i is None else i,x))})
      df['ztsfdm']=df.index
      df.index=range(len(df))
      df['ztsfdm']=df[['ztsfdm']].applymap(lambda x:x.strip())
      df3=db_query(sqlx)
      dfy3=db_query(sqly)
      df3=pd.concat([df3,dfy3],ignore_index=True) 
      
      #df1=db_query(sql2)
      #df2=db_query(sql)
      #df3=pd.merge(df1,df2,on='jgmc')
      #df3=pd.merge(df1,df2,on='jgdm')
      #df3=pd.concat([df3,df31],ignore_index=True).drop_duplicates()
      df=pd.merge(df3,df,on='ztsfdm')
      df.insert(7,'sh1',df['sh'])
      del df['sh']
      del df['ztsfdm']
      df['t4']=df[['t4']].applymap(sbzt)
      df.columns=['机构代码','机构名称','注册资金','货币种类','注册资金_人民币','企业类型','股东信息','所属行业','成立日期','开始投保年月','最后投保年月','社保缴纳情况']
      
      return df

def sbzt(x):
     if x>3: return '社保缴交不正常'
     if x==3: return '社保停缴3个月'
     if x==2: return '社保停缴2个月'
     if x==1: return  '社保停缴1个月'
     else: return '正常'

def getdf_gjj(enddate,xzqh):
      #enddate='2016-09-01'
      xzqh=qh[xzqh]
      sql="""
           SELECT socialcreditcode as jgdm  
           , min(beginpaydate) t3 
           ,max(lastpaydate) t2
           ,datediff(mm,max(lastpaydate),'%s')-1 t4 
            FROM providentfund.dbo.t_gjj_cl
            group by socialcreditcode having datediff(mm,max(lastpaydate),'%s')>1
            """%(enddate,enddate)
      sql2="""
            select  ztsfdm,jgdm,jgmc,zczj,hbzl,zczj_rmb,qylx,jjhy from basedb.dbo.t_zzjgjz where (jgdm in(select jgdm from(%s) tt )) 
            and ztztdm>=0 and jglxdm in('1','2')  
             and xzqhdm='%s' and ((qylxdm not like '[567w]%%' and zczj_rmb>=10000) or (qylxdm like '[567w]%%' and zczj_rmb>=3100))
            """%(sql,xzqh)
      sqlx="""
            select ztsfdm,a.jgdm,a.jgmc,zczj,hbzl,zczj_rmb,qylx,jjhy,rq,b.t3,b.t2,b.t4 from
            (select  ztsfdm,jgdm,jgmc,zczj,hbzl,zczj_rmb,qylx,jjhy,convert(varchar(100),clrq,23) as rq from basedb.dbo.t_zzjgjz where  
            ztztdm>=0 and jglxdm in('1','2')  
            and xzqhdm='%s' and ((qylxdm not like '[567w]%%' and zczj_rmb>=10000) or (qylxdm like '[567w]%%' and zczj_rmb>=3100))) a,
            (%s) b where a.jgdm=b.jgdm 
            """%(xzqh,sql)

      sql3="""
          select * from(
          select entid,'{'+shname+'-出资额:'+ltrim(str(capamt,10,4))+'-股份:'+ltrim(str(capprop,9,2))+'%%}'  
          as sh from regdb.dbo.tdsh where entid in(select ztsfdm from (%s) tt) 
          and  entstatuscode=0 ) aaaa where sh is not null
          """%(sql2)
        
      df=db_query(sql3)
      df=df.groupby('entid').agg({'sh':lambda x: ','.join(map(lambda i:'' if i is None else i,x))})
      df['ztsfdm']=df.index
      df.index=range(len(df))
      df['ztsfdm']=df[['ztsfdm']].applymap(lambda x:x.strip())
      df3=db_query(sqlx)
      #df1=db_query(sql2)
      #df2=db_query(sql)
      #df3=pd.merge(df1,df2,on='jgmc')
      #df3=pd.merge(df1,df2,on='jgdm')
      #df3=pd.concat([df3,df31],ignore_index=True).drop_duplicates()
      df=pd.merge(df3,df,on='ztsfdm')
      df.insert(7,'sh1',df['sh'])
      del df['sh']
      del df['ztsfdm']
      df['t4']=df[['t4']].applymap(gjjzt)
      df.columns=['机构代码','机构名称','注册资金','货币种类','注册资金_人民币','企业类型','股东信息','所属行业','成立日期',
                '公积金开始缴交年月','公积金最后缴交年月','公积金缴纳情况']
      
      return df


def gjjzt(x):
     if x>3: return '公积金缴交不正常'
     if x==3: return '公积金停缴3个月'
     if x==2: return '公积金停缴2个月'
     if x==1: return  '公积金停缴1个月'
     else: return '正常'

#-------------------------------------------------------------5:战略新兴产业------------------------------------------------------------------------------
#行业代码与行业分类的映射

def jr(x):
     if len(str(x))<3 : return '其它'
     if len(str(x))>=3:x=str(x)
     if x[0:3]=='J66':return '货币金融服务'
     if x[0:3]=='J67': return '资本市场服务'
     if x[0:3]=='J68': return '保险业'
     else: return '其它金融业'
     
def wh(x):
     if len(str(x))<3 : return '其它'
     if len(str(x))>=3:x=str(x)
     if x[0:3]=='R85':return '新闻和出版业'
     if x[0:3]=='R86': return '广播、电视、电影和影视录音制作业'
     if x[0:3]=='R87': return '文化艺术业'
     if x[0:3]=='R88': return '体育'
     if x[0:3]=='R89': return '娱乐业'
     return '文化艺术业'


     
def getdf_xxhy(startdate,enddate,xzqh):
     xz=xzqh
     xzqh=qh[xzqh]
     
     sql="""
        select jgmc as '机构名称',jglx as '机构类型', 
        fddbr as '法定代表人人',jgdhhm as '固定电话',jgmobile as '移动电话', 
        jgdz as '机构地址', 
        convert(varchar(100),clrq,23) as '成立日期',zczj_rmb as '注册资金',zgrs as '职工人数', 
        jyfw as  '机构简介', 
        a.jjhy as '所属行业',a.jjhydm 
        from BaseDB.dbo.t_zzjgjz a 
        where 
        clrq>='%s' and clrq<'%s' 
        and  XZQHdm='%s'  
        and jglxdm in('1','2')"""%(startdate,enddate,xzqh)
     df=db_query(sql)
     
     #金融业
     sql1="""
        select jgmc as '机构名称',jglx as '机构类型', 
        fddbr as '法定代表人人',jgdhhm as '固定电话',jgmobile as '移动电话', 
        jgdz as '机构地址', 
        convert(varchar(100),clrq,23) as '成立日期',zczj_rmb as '注册资金',zgrs as '职工人数', 
        jyfw as  '机构简介', 
        a.jjhy as '所属行业',a.jjhydm  
        from BaseDB.dbo.t_zzjgjz a 
        where 
        clrq>='%s' and clrq<'%s' 
        and  XZQHdm='%s'  
        and substring(a.jjhydm,1,1)='J'
        and jglxdm in('1','2')"""%(startdate,enddate,xzqh)
     

     df1=db_query(sql1)
     df1['新行业类别']=df1[['jjhydm']].applymap(jr)
     df1['行业大类']='金融业'

     #文化创意
     sql2="""
        select jgmc as '机构名称',jglx as '机构类型', 
        fddbr as '法定代表人人',jgdhhm as '固定电话',jgmobile as '移动电话', 
        jgdz as '机构地址', 
        convert(varchar(100),clrq,23) as '成立日期',zczj_rmb as '注册资金',zgrs as '职工人数', 
        jyfw as  '机构简介', 
        a.jjhy as '所属行业',a.jjhydm  
        from BaseDB.dbo.t_zzjgjz a 
        where ztztdm>=0 and jglxdm in('1','2')  
         
        and substring(jjhydm,2,4) in ('5143','5144','5145','5243','5244', 
        '7350','9421','6420','6319','6321','6322','6330','6510','6591','7482','7491','7851','7852','7712','7713','7492','2431','2432', 
          '2433','2434','2435','2436','2437','2438','2439','3079','5146','5245','5246','7250','2311','2312','2319','2320','2330', 
        '5181','5182','7121','7122','7123','7292','7299','2411','2412','2414','2421','2422','2423','2429','2450','2461','2462', 
        '2469','3951','3952','3953','2672','2221','2222','2642','2643','2664','3872','3990','5141','5241','5247','5248','5137','5271', 
          '5149','5249','3542','3931','3932','3939','3471','3472','3473','3474','5178','5176') 
        and (jgmc+jyfw like '%%文化%%' or jgmc+jyfw like '%%教育%%' or jgmc+jyfw like '%%广告%%' or jgmc+jyfw like '%%娱乐%%') 
        and clrq>='%s' and clrq<'%s' and xzqhdm='%s' 
        """%(startdate,enddate,xzqh)
     df2=db_query(sql2)
    

     sql21="""
        select jgmc as '机构名称',jglx as '机构类型', 
        fddbr as '法定代表人人',jgdhhm as '固定电话',jgmobile as '移动电话', 
        jgdz as '机构地址', 
        convert(varchar(100),clrq,23) as '成立日期',zczj_rmb as '注册资金',zgrs as '职工人数', 
        jyfw as  '机构简介', 
        a.jjhy as '所属行业',a.jjhydm  
        from BaseDB.dbo.t_zzjgjz a 
        where 
        clrq>='%s' and clrq<'%s' 
        and  XZQHdm='%s'  
        and substring(a.jjhydm,1,1)='R'
        and jglxdm in('1','2')"""%(startdate,enddate,xzqh)
     df21=db_query(sql21)
     df2=pd.concat([df2,df21],ignore_index=True)
     df2['新行业类别']=df2[['jjhydm']].applymap(wh)
     df2['行业大类']='文化创意'
      

     #专门专业
     df3=getdf_fuwu(startdate,enddate,xz)
     df3['行业大类']='专门专业(服务业)'


     #战略新兴产业
     #生物产业
     df4a=df[df['机构名称'].str.contains('生物')]
     
     df4a1=df[df['机构简介'].str.contains('生物.*生物|生物技术\S发|生物科技')]
     df4a=pd.concat([df4a,df4a1],ignore_index=True)
     df4a=df4a.drop_duplicates()
     df4a['新行业类别']='生物产业'
     #节能环保产
     df4b=df[df['机构名称'].str.contains('环保|节能')]
     
     df4b1=df[df['机构简介'].str.contains('节能.*环保|环保设备|环保检测|再生资源|环保工程|环保.*环保|节能.*节能')]
     df4b=pd.concat([df4b,df4b1],ignore_index=True)
     df4b=df4b.drop_duplicates()
     df4b['新行业类别']='节能环保'
     #高端装备业c 船舶制造 航天 卫星 轨道交通 海洋工程 智能装备
     df4c=df[df['机构名称'].str.contains('船舶制造|航天.*科技|海洋工程|轨道交通|卫星')]
     
     df4c1=df[df['机构简介'].str.contains('船舶制造|航天.*科技|海洋工程|轨道交通|智能装备')]
     df4c=pd.concat([df4c,df4c1],ignore_index=True)
     df4c=df4c.drop_duplicates()
     df4c['新行业类别']='高端装备业'
     
     #新能源产业d
     df4d=df[df['机构名称'].str.contains('新能源')]
     df4d2=df[df['机构名称'].str.contains('能源')]
     df4d1=df[df['机构简介'].str.contains('新能源')]
     df4d=pd.concat([df4d,df4d1],ignore_index=True)
     df4d=df4b.drop_duplicates()
     df4d=df4d[df4d['机构名称'].str.contains('(?!汽车)')]
     df4d['新行业类别']='新能源产业'


     
     #新一代信息技术g 云计算  信息安全  操作系统 大数据 高端软件 大型数据库
     df4g=df[df['机构名称'].str.contains('云计算|信息安全|大数据|操作系统|高端软件')]
     
     df4g1=df[df['机构简介'].str.contains('云计算|信息安全|大数据|操作系统|高端软件|大型数据库')]
     df4g=pd.concat([df4g,df4g1],ignore_index=True)
     df4g=df4g.drop_duplicates()
     df4g['新行业类别']='新一代信息技术'
     
                                   
     

     #新材料产业e
     df4e=df[df['机构名称'].str.contains('新材料')]

     df4e1=df[df['机构简介'].str.contains('高分子|硅.*材料|稀土|树脂|高性能\S料|无机非金属|有机.{1-3}材料')]
     df4e=pd.concat([df4e,df4e1],ignore_index=True)
     df4e=df4e.drop_duplicates()
     df4e['新行业类别']='新材料产业'
    

     #系能源汽车产业f
     df4f=df[df['机构简介'].str.contains('新能源汽车')]
     df4f['新行业类别']='新能源汽车'
     
     df4s=[df4a,df4b,df4c,df4d,df4e,df4f,df4g]
     df4=pd.concat(df4s,ignore_index=True)
     df4['行业大类']='战略新兴产业'
     word=list(df3.columns)
     df1=shift(df1,word)
     df2=shift(df2,word)
     df4=shift(df4,word)

     dfx=pd.concat([df1,df2,df3,df4],ignore_index=True)
     

                                   
     

     
     dfss=[[df],[df1],[df2],[df3],[df4],[dfx]]
     return  dfss



#-------------------------------------------------------------6 :增资本表----------------------------------------------------------------------------------

def getdf_zengzi(startdate,enddate,xzqh='福田区'):
     xzqh='福田区'
     df=getdf_zz(startdate,enddate,xzqh)
     return df

def getdf_zz(startdate,enddate,xzqh):
     #startdate='2016-09-01'
     #enddate='2016-10-01'
     #xzqh='福田区
     
     dz=xzqh[:-1]
     sql0="""select entid from regdb.dbo.tdalteritem where alteritemcode in('17')  
            and alterdate>='%s' and alterdate<'%s'"""%(startdate,enddate)
     sql="""
        select entid,addr,regcap,authdate,rnx 
        from( 
        select  
        aa.entid,aa.addr,aa.regcap,aa.authdate as authdate ,bb.authdate as authdate1,row_number() over(partition BY 
        aa.entid order by aa.authdate desc) as rnx 
        from RegDB.dbo.tdbase aa , 
        (
        select a.entid,addr,regcap,authdate 
        from(
        select entid,addr,regcap,authdate from regdb.dbo.tdbase) a , 
        (select * from(select entid,alterdate ,alteritemcode,row_number() over (partition by entid order by alterdate desc) as rn 
         from RegDB.dbo.tdalteritem 
        where  alteritemcode in('17')  and alterdate>='%s'  
        and alterdate<'%s' ) bx  where rn=1) b 
        where a.entid=b.entid and a.authdate=b.alterdate)  bb 
        where  aa.authdate<=bb.authdate and aa.entid=bb.entid  and aa.authdate<'%s'  
        and aa.entid in(select entid from regdb.dbo.tdalteritem where alteritemcode in('17') 
        and alterdate>='%s' and alterdate<'%s')) tt 
        where rnx in(1,2) 
        """%(startdate,enddate,enddate,startdate,enddate)
     sql1="""select tt1.entid,tt1.regcap as  '变更前注册资金',tt2.regcap as '变更后注册资金',convert(varchar(100),tt2.authdate,23) as '变更日期', 
         tt2.regcap-tt1.regcap as '增资'
        from(%s  and rnx=2) tt1,(%s and rnx=1) tt2 where 
        tt2.addr like '%%%s%%' and tt1.entid=tt2.entid  """%(sql,sql,dz)


     sql2="""select EntID ,SHName as '股东名称',CapAmt as '出资额',CapProp as '出资比例' from [CLUSTER2014DB2\MSSQLSERVER2].[regDB].[dbo].[tdSH]  
         where EntID  in(%s) and entstatuscode=0"""%(sql0)
     ##
     sql3="""
         select entid, [股东信息]= '{'+[股东名称]+'-'+'出资额:'+ltrim(str([出资额],10,2))+'(万元)-'+'出资比例:'
         +ltrim(str([出资比例],9,4))+'%%}'  
            from (%s) t  """%(sql2)
     sql4="""select ztsfdm as entid,tydm as '统一社会信用代码',jgdm as '组织机构代码',zch as '注册号', 
            jgmc as '企业名称',fddbr '法人名称',jgdz as '机构地址',jyfw as '经营范围',convert(varchar(50),clrq,23) as '成立日期',convert(varchar(50),jyqx,23) as '经营期限止',
            hbzl as '货币种类',qylx as '企业类型',jjhydm as '行业代码',jjhy as '行业类型' from basedb.dbo.t_zzjgjz 
            where jglxdm in('1','2') and ztsfdm in(%s) """%sql0
     df3=db_query(sql4)
     df1=db_query(sql3)
     dff=df1.groupby('entid').agg({'股东信息':lambda x:','.join(map(lambda i:'' if i is None else i,x))})
     dff['entid']=dff.index
     dff['entid']=dff[['entid']].applymap(lambda x:x.strip())
     dff.index=range(len(dff))
     df2=db_query(sql1)
     df2['entid']=df2[['entid']].applymap(lambda x:x.strip())
     df=pd.merge(df2,dff,on='entid',how='left')
     
     df=pd.merge(df3,df,on='entid')
     a=['entid', '统一社会信用代码', '组织机构代码', '注册号', '企业名称', '法人名称', '机构地址', '经营范围',
       '成立日期','经营期限止', '变更前注册资金', '变更后注册资金','增资', '变更日期', '货币种类', '企业类型', '行业代码', '行业类型',
        '股东信息']
     df=shift(df,a)

     #df['entid']=df[['entid']].applymap(lambda x:'\''+x)
     #df['注册号']=df[['注册号']].applymap(lambda x: '\''+x)
     #df['组织机构代码']=df[['组织机构代码']].applymap(lambda x:'\''+x)
     #df['统一社会信用代码']=df[['统一社会信用代码']].applymap(lambda x:'\''+x)
     return df

#-------------------------------------------------------------7:统计表------------------------------------------------------------------------------------


#福田商事主体总量
#取全部记录成立时间-注销时间（未吊销写为2050-01-01
def getdf_authdates(jglxdm=['1','2'],xzqh='全市'):
     
     word=list(map(lambda x:'\'%s\''%x,jglxdm))
     jglxdm='('+','.join(word)+')'
     if xzqh=='全市':
         sql="""
            select ztsfdm,,ztztdm, convert(varchar(50),clrq,23) as clrq,case when authdate is null then '2050-01-01' else convert(varchar(50),authdate,23) end as
             authdate from BaseDB.dbo.t_zzjgjz left join ( 
            select DISTINCT entid,first_value(authdate)over(partition by entid order by authdate desc) as authdate 
            from regdb.dbo.tdbase where entstatuscode <0 ) tt on ztsfdm=entid where jglxdm in%s  and ztsfdm is not null  
            """%(jglxdm)
     else:
         xzqh=qh[xzqh]
         sql="""
            select ztsfdm,ztztdm, convert(varchar(50),clrq,23) as clrq,case when authdate is null then '2050-01-01' else convert(varchar(50),authdate,23) end as
            authdate from BaseDB.dbo.t_zzjgjz left join ( 
            select DISTINCT entid,first_value(authdate)over(partition by entid order by authdate desc) as authdate 
            from regdb.dbo.tdbase where entstatuscode <0 ) tt on ztsfdm=entid where jglxdm in%s and xzqhdm='%s' and ztsfdm is not null 
            """%(jglxdm,xzqh)
     df=db_query(sql)
     df=df.drop_duplicates()
     return df

def getdf_bs(jglxdm,enddate,xzqh='福田区'):
     df=getdf_authdates(jglxdm,xzqh)
     dates=[]
     counts=[]
     date1=datetime.datetime.strptime(enddate,'%Y-%m-%d').date()
     
     
     for i in range(-5,1):
          date=add_months(date1,i)
          date=datetime.datetime.strftime(date,'%Y-%m-%d')
          dates.append(date)
     for date in dates:
          df1=df[(df['clrq']<date) & (df['authdate']>=date)]
          a=len(df1)
          counts.append(a)
     data=[(a,b) for (a,b) in zip(dates,counts)]
     if jglxdm==['1','2','B']:name='主体总数量'
     if jglxdm==['1','2']: name='企业数量'
     if jglxdm==['B']: name='个体户数量'
     df=pd.DataFrame(data,columns=['截止日期',name])
     return df

def getdf_p1(enddate,xzqh='福田区'):
     dms=[['1','2','B'],['1','2'],['B']]
     dfs=[]
     for jglxdm in dms:
          df=getdf_bs(jglxdm,enddate,xzqh)
          dfs.append(df)
     df=pd.merge(dfs[0],dfs[1],on='截止日期')
     df=pd.merge(df,dfs[2],on='截止日期')
     df['企业占比']=df['企业数量']/df['主体总数量']
     df['个体户占比']=df['个体户数量']/df['主体总数量']
     a=df.pop('企业占比')
     b=df.pop('个体户占比')
     df.insert(3,'企业占比',a)
     df.insert(5,'个体户占比',b)
     return df
          
#统计每月新增企业同比
def getdf_zl(jglxdm,enddate,xzqh='福田区'):
     df=getdf_authdates(jglxdm,xzqh)
     dates=[]
     counts=[]
     date1=datetime.datetime.strptime(enddate,'%Y-%m-%d').date()
     
     
     for i in range(-12,1):
          date=add_months(date1,i)
          date=datetime.datetime.strftime(date,'%Y-%m-%d')
          dates.append(date)
     for i in range(12):
          df1=df[(df['clrq']<dates[i+1]) & (df['clrq']>=dates[i])]
          a=len(df1)
          counts.append(a)
     data=[(a,b) for (a,b) in zip(dates[:-1],counts)]
     if jglxdm==['1','2','B']:name='主体月增量'
     if jglxdm==['1','2']: name='企业月增量'
     if jglxdm==['B']: name='个体户月增量'
     df=pd.DataFrame(data,columns=['统计月份',name])
     return df


def getdf_p2(enddate,xzqh='福田区'):
     dms=[['1','2','B'],['1','2'],['B']]
     dfs=[]
     for jglxdm in dms:
          df=getdf_zl(jglxdm,enddate,xzqh)
          dfs.append(df)
     df=pd.merge(dfs[0],dfs[1],on='统计月份')
     df=pd.merge(df,dfs[2],on='统计月份')
     df['企业月增比']=df['企业月增量'].pct_change()
     df['个体户月增比']=df['个体户月增量'].pct_change()
     df['主体月增比']=df['主体月增量'].pct_change()
     a=df.pop('企业月增比')
     b=df.pop('个体户月增比')
     c=df.pop('主体月增比')
     df.insert(3,'企业月增比',a)
     df.insert(5,'个体户月增比',b)
     df.insert(2,'主体月增比',c)
     return df


#内外资 资金总额等
def getdf_p3(enddate,xzqh='福田区'):
     dates=[]
     counts=[]
     f1s=[]
     f2s=[]
     date1=datetime.datetime.strptime(enddate,'%Y-%m-%d').date()
     
     
     for i in range(-6,1):
          date=add_months(date1,i)
          date=datetime.datetime.strftime(date,'%Y-%m-%d')
          dates.append(date)
     for i in range(6):
          df=getdf_xzz(dates[i],dates[i+1],xzqh)
          df=df[df['机构类型']=='企业']
          a1=len(df)
          a2=len(df[df['内外资']=='内资'])
          a3=a2/a1
          a4=df['注册资金'][df['内外资']=='内资'].sum()
          b2=len(df[df['内外资']=='内资'])
          b3=b2/a1
          b4=df['注册资金'][df['内外资']=='内资'].sum()
          c=len(df[(df['内外资']=='内资') &(df['注册资金']>=10000)])
          d=len(df[(df['内外资']=='外资') &(df['注册资金']>=3100)])

          df1=df[['注册公司名称','注册资金']][(df['内外资']=='内资') &(df['注册资金']>=10000)].head(5)
          f1=list(df1['注册公司名称']+':'+(df1['注册资金']/10000).astype(str)+'亿')
          
          df2=df[['注册公司名称','注册资金']][(df['内外资']=='外资') &(df['注册资金']>=3100)].head(5)
          f2=list(df2['注册公司名称']+':'+df2['注册资金'].astype(str)+'万元')
          f1s.append(f1)
          f2s.append(f2)
          counts.append([a1,a2,a3,a4,b2,b3,b4,c,d])
     data=[[a]+b for a,b in zip(dates[:-1],counts)]
     df=pd.DataFrame(data)
     df.columns=['统计月份','企业总数量','内资数量','内资占比','内资资金和(万)','外资数量','外资占比','外资资金和(万)','内资(亿上)数','外资(大型)数']

     data1=[[a]+b for a,b in zip(dates[:-1],f1s)]
     data2=[[a]+b for a,b in zip(dates[:-1],f2s)]
     df1=pd.DataFrame(data1)
     df2=pd.DataFrame(data2)
     return [df,df1,df2]



#新增企业行业的排名
def getdf_p4(enddate,xzqh='福田区'):
     dates=[]
     date1=datetime.datetime.strptime(enddate,'%Y-%m-%d').date()
     dfs=[]
     
     for i in range(-6,1):
          date=add_months(date1,i)
          date=datetime.datetime.strftime(date,'%Y-%m-%d')
          dates.append(date)
     for i in range(6):
          df=getdf_xzz(dates[i],dates[i+1],xzqh)
          df=df[df['机构类型']=='企业']
          df1=df.groupby('行业大类').size()
          df1=pd.DataFrame({'行业大类':df1.index,'总数':df1.values})

          df1['统计月份']=dates[i]
          dfs.append(df1)
     df=pd.concat(dfs,ignore_index=True)
     df=pd.pivot_table(df,index=['统计月份'],columns=['行业大类'])
     df.columns=df.columns.get_level_values(1)
     df=df[['批发和零售业','租赁和商务服务业','科学研究和技术服务业','住宿和餐饮业','信息传输、软件和信息技术服务业','建筑业','房地产业']]
     pops=[]
     for w in df.columns:
          pops.append(df[w].pct_change())
     for  i in range(len(pops)):
          df.insert(2*i+1,'月增幅%d'%i,pops[i])

     df.insert(0,'统计月份',df.index)
     df.index=range(len(df))
     
     
     return df



#当月行业-内外资统计
def getdf_p5(enddate,xzqh='福田区'):
     date1=datetime.datetime.strptime(enddate,'%Y-%m-%d').date()
     dfs=[]
     dates=[]
     
     for i in range(-1,1):
          date=add_months(date1,i)
          date=datetime.datetime.strftime(date,'%Y-%m-%d')
          dates.append(date)
     df=getdf_xzz(dates[0],dates[1],xzqh)
     df=df[df['机构类型']=='企业']
     df.index=range(len(df))
     df['k']=1
     df['sl']='其它'
     df.loc[(df['内外资']=='内资') &(df['注册资金']>=10000),'sl']='一亿以上内资'
     df.loc[(df['内外资']=='外资') &(df['注册资金']>=3100),'sl']='1000万以上外资'
     df1=pd.pivot_table(df,index=['行业大类'],columns=['内外资'],values=['k'],aggfunc=[np.sum])
     df1.columns=df1.columns.get_level_values(2)
     df1.insert(0,'行业大类',df1.index)
     df2=pd.pivot_table(df,index=['行业大类'],columns=['sl'],values=['k'],aggfunc=[np.sum])
     df2.columns=df2.columns.get_level_values(2)
     df2.insert(0,'行业大类',df2.index)
     df=pd.merge(df1,df2,on='行业大类')
     df=df.fillna(0)
     
     return df
#-----------------------------------------------------------A:辅助功能模块--------------------------------------------------------------------------------
def add_months(dt,months):
    month = dt.month - 1 + months
    if month>=0:
         year = dt.year + int(month / 12)
    else:
          year = dt.year + int(month / 12)-1
    month = int(month % 12 + 1)
    day = min(dt.day,calendar.monthrange(year,month)[1])
    return dt.replace(year=year, month=month, day=day) 


def shift(df,key):
     word=df.columns
     for w in word:
          if w not in key:
               del df[w]
     i=0
     for w in key:
          b=df.pop(w)
          df.insert(i,w,b)
          i+=1
     return df


def jiancedate():
     sql="""
        select max(rq) from( 
        SELECT ZJTBN+'-'+ZJTBY as rq,count(*) as ct FROM sbsj.[RESMG].[GGXY_QYCBXX108635] 
        group by ZJTBN+'-'+ZJTBY  
        having count(*)>100000) aa 
        """
     date1=db_query(sql).iat[0,0]
     date1=date1+'-01'
     d1=datetime.datetime.strptime(date1,'%Y-%m-%d').date()
     d1=add_months(d1,1)
     date1=str(d1)
     sql1="""
        select max(rq) from( 
        SELECT substring(lastpaydate,1,7) rq,count(*) as ct FROM providentfund.[dbo].[T_Gjj_Cl] 
        group by substring(lastpaydate,1,7) 
        having count(*)>2000) ss 
        """
     date2=db_query(sql1).iat[0,0]
     date2=date2+'-01'
     d2=datetime.datetime.strptime(date2,'%Y-%m-%d').date()
     d2=add_months(d2,1)
     date2=str(d2)
 
     return [date1,date2]
#-----------------------------------------------------------B:成果表输出模块--------------------------------------------------------------------------------------
#1.专业服务
def t_fuwu(startdate,enddate,path,xzqh='福田区'):
      a=datetime.datetime.strptime(startdate,'%Y-%m-%d').date()
      x=a.month
      y=datetime.datetime.strftime(a,'%Y%m')
      #a=add_months(a,1)
      #enddate=str(a)
      df1=getdf_fuwu(startdate,enddate,xzqh)
      a=add_months(a,-2)
      startdate=str(a)
      df2=getdf_fuwu(startdate,enddate,xzqh)
      dfs=[[df1],[df2]]
      sheets=['%d月份'%x,'%d-%d-%d月份'%(x-2,x-1,x)]
      name='附件1、%s专业服务机构信息%s'%(xzqh,y)
      pt=yourpath(name,path)
      outdfss(dfs,sheets,pt)
      return [pt.replace(path,''),sheets]

#2.新增大企业
def t_xinzeng(startdate,enddate,path,xzqh):
     b=datetime.datetime.strptime(startdate,'%Y-%m-%d').date()
     b1=datetime.datetime.strptime(enddate,'%Y-%m-%d').date()
     delta=round((b1-b).days/30)
     m=[]
     m1=[]
     for i in range(delta):
          w=str(b.month)
          w1=datetime.datetime.strftime(b,'%Y%m')
          m.append(w)
          m1.append(w1)
          b=add_months(b,1)
     x='-'.join(m)
     y='-'.join(m1)
     print(startdate,enddate,xzqh)
     df1=getdf_xz(startdate,enddate,xzqh)
     df2=getdf_daxing_nei(startdate,enddate,xzqh)
     df3=getdf_daxing_wai(startdate,enddate,xzqh)
     dfs=[[df1],[df2],[df3]]
     sheets=['%s%s月新增企业'%(xzqh,x),'%s内资一亿以上'%(xzqh),'%s外资500万美元以上'%(xzqh)]
     name='附件2、%s新增大企业信息%s'%(xzqh,y)
     pt=yourpath(name,path)
     outdfss(dfs,sheets,pt)
     return [pt.replace(path,''),sheets]


#3.迁移
def t_qianyi(startdate,enddate,path,xzqh,qianyi='迁出'):
     df1=getdf_nei(startdate,enddate,xzqh)
     if qianyi=='迁出':df1=df1[df1['迁移状态']=='%s迁出到市内'%xzqh]
     if qianyi=='迁入':df1=df1[df1['迁移状态']=='市内迁入%s'%xzqh]
     a=['统一社会信用代码','组织机构代码','注册号','企业名称','注册资金','货币种类','企业类型','股东信息','变更日期','行业类型','变更前地址'
     ,'变更后地址','迁移状态']
     a1=['统一社会信用代码', '组织机构代码', '注册号','企业名称','注册地址','注册资金','货币种类','企业类型','股东信息','核准日期','经济行业'
     ,'迁移信息','主体记录状态']
     df1=shift(df1,a)
     df2=getdf_wai(startdate,enddate,xzqh)
     df2=shift(df2,a1)
     dfs=[[df1],[df2]]
     b=datetime.datetime.strptime(startdate,'%Y-%m-%d').date()
     b1=datetime.datetime.strptime(enddate,'%Y-%m-%d').date()
     delta=round((b1-b).days/30)
     m=[]
     m1=[]
     for i in range(delta):
          w=str(b.month)
          w1=datetime.datetime.strftime(b,'%Y%m')
          m.append(w)
          m1.append(w1)
          b=add_months(b,1)     
     x='-'.join(m)
     y='-'.join(m1)
     sheets=['%s月%s迁出到市内其它地区'%(x,xzqh),'%s月%s迁出到市外'%(x,xzqh)]
     name='附件3、%s企业迁移信息%s'%(xzqh,y)
     pt=yourpath(name,path)
     outdfss(dfs,sheets,pt)
     return [pt.replace(path,''),sheets]

#4.社保公积金监测
def t_jiance(enddate1,enddate2,enddate,path,xzqh='福田区'):
     df1=getdf_sb(enddate1,xzqh)
     df2=getdf_gjj(enddate2,xzqh)
     dfs=[[df1],[df2]]
     rq=datetime.datetime.strptime(enddate,'%Y-%m-%d').date()
     rq=add_months(rq,-1)
     rq=datetime.datetime.strftime(rq,'%Y%m')
     
     sheets=['社保监测','公积金监测']
     name='附件4、%s企业监测信息%s'%(xzqh,rq)
     pt=yourpath(name,path)
     outdfss(dfs,sheets,pt)
     return [pt.replace(path,''),sheets]

#5.战略新兴产业
def t_xxhy(startdate,enddate,path,xzqh='福田区'):
      a=datetime.datetime.strptime(startdate,'%Y-%m-%d').date()
      x=a.month
      y=datetime.datetime.strftime(a,'%Y%m')
      #a=add_months(a,1)
      #enddate=str(a)
      
      dfs=getdf_xxhy(startdate,enddate,xzqh)
      sheets=['新增总表','金融业','文化创意','专门专业','战略新兴产业','四大产业和']
      
      name='附件5、%s战略新兴产业%s'%(xzqh,y)
      pt=yourpath(name,path)
      outdfss(dfs,sheets,pt)
      return [pt.replace(path,''),sheets]

#6.增资表
def t_zengzi(startdate,enddate,path,xzqh='福田区'):
      a=datetime.datetime.strptime(startdate,'%Y-%m-%d').date()
      x=a.month
      y=datetime.datetime.strftime(a,'%Y%m')
      #a=add_months(a,1)
      #enddate=str(a)
      df1=getdf_zengzi(startdate,enddate,xzqh)
      dfs=[[df1]]
      sheets=['%d月份增资'%x]
      
      name='附件6、%s增资%s'%(xzqh,y)
      pt=yourpath(name,path)
      outdfss(dfs,sheets,pt)
      return [pt.replace(path,''),sheets]

#7.统计表
def t_state(startdate,enddate,path,xzqh='福田区'):
      a=datetime.datetime.strptime(startdate,'%Y-%m-%d').date()
      x=a.month
      y=datetime.datetime.strftime(a,'%Y%m')
      #a=add_months(a,1)
      #enddate=str(a)
      df1=getdf_p1(enddate,xzqh)
      df2=getdf_p2(enddate,xzqh)
      df3=getdf_p3(enddate,xzqh)
      df4=getdf_p4(enddate,xzqh)
      df5=getdf_p5(enddate,xzqh)
      dfs=[[df1],[df2],df3,[df4],[df5]]
      sheets=['总体概况','新增企业同比','内外资 资金总额等','新增企业行业的排名','当月行业-内外资统计']
      
      name='附件7、%s月度简析统计报%s'%(xzqh,y)
      pt=yourpath(name,path)
      outdfss(dfs,sheets,pt)
      return [pt.replace(path,''),sheets]







#-----------------------------------------------------T:test测试模块--------------------------------------------------