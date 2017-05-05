#此文件用于逆向迭代出街道


from sistdmyy import db 
from sistdmyy.dz import mine 
from sistdmyy.dz.dz_std import std 


#class jgtrain 是用来 得到dz_std_jdtrain(dz_std1)表,拿来做训练的是jgdz中含街道的

class jdtrain:
    def __init__(self):
        self.m=db()
    def p_corpus(self):
        sql="""

        IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID('test_dmyy.dbo.dz_std_jdcorpus') AND type in ('U'))
        DROP TABLE test_dmyy.dbo.dz_std_jdcorpus;
        with t1 as (select * from test_dmyy.dbo.dz_jd)
        ,t2 as (
        select ztsfdm,jgdz,word
        ,row_number() over( partition by ztsfdm order by len(word) desc) rn
         from basedb.dbo.t_zzjgjz  as a,t1
        where charindex(t1.word,jgdz)>0 and ztztdm>=0 and jglxdm in('1','2'))
        ,t3 as (select substring(word,1,len(word)-2)+'办事处' as word from test_dmyy.dbo.dz_jd where word!='前海深港合作区')


        ,t4 as (
        select ztsfdm,jgdz,word
        ,row_number() over( partition by ztsfdm order by len(word) desc) rn
         from basedb.dbo.t_zzjgjz  as a,t3
        where charindex(t3.word,jgdz)>0 and ztztdm>=0 and jglxdm in('1','2'))
        , t5 as(
        select ztsfdm,jgdz,substring(word,1,len(word)-3)+'街道' as word,rn from t4
        union 
        select * from t2)

        select * into test_dmyy.dbo.dz_std_jdcorpus from t5 where rn=1

        """
        self.m.update_sql(sql)
        x=self.m.frommssql("select count(*) from test_dmyy.dbo.dz_std_jdcorpus ")
        print("表dz_std_jdcorpus 更新完毕,共%d行"%x.iat[0,0])

    def p_stdtrain(self,sql=None):
        if sql is None:
            sql="select  ztsfdm,jgdz from test_dmyy.dbo.dz_std_jdcorpus"
        p=std(sql)
        p.tb()
        print(len(p.df))
        self.m.tomssql(p.df,'dz_std_jdtrain')

    def p_update(self):
        sql="""
        update  test_dmyy.dbo.dz_std_jdtrain

        set [街道]=t2.word

        from test_dmyy.dbo.dz_std_jdtrain as t1,test_dmyy.dbo.dz_Std_jdcorpus as t2

        where t1.ztsfdm=t2.ztsfdm and t1.ztsfdm is not null
        """
        self.m.update_sql(sql)

    def p_all(self):
        self.p_corpus()
        self.p_stdtrain()
        self.p_update()

#jd_predict是用来讲一个带ztsfdm和jgdz的df处理成dz_sist_jd的形式

class jd_predict:

    def __init__(self):
        self.m=db()
        sql="select * from test_dmyy.dbo.dz_std1"
        self.df=self.m.frommssql(sql)

    def p_df(self,sql0=None):
        #第一部分通过关键字
        if sql0 is None:
            sql0="""
            select  ztsfdm,jgdz from basedb.dbo.t_zzjgjz where ztsfdm is not null and jgdz is not null 
            and clrq>='2016-01-01'
            """
        sql="""
        with a as (%s )
        ,b as (
        select *
        ,row_number() over(partition by ztsfdm order by len(word) desc) as rn
        from a left join test_dmyy.dbo.dz_jd t on charindex(t.word,a.jgdz)>0 
         or charindex(substring(t.word,1,len(t.word)-2)+'办事处',a.jgdz)>0)
        select ztsfdm,jgdz,word from b where rn=1
        """%sql0
        df_1=self.m.frommssql(sql)
        print('第一部分，完成')
        #第二部分，无关键字，通过逆向迭代
        df1=df_1.loc[df_1['word'].isnull(),['ztsfdm','jgdz']]
        print('第二部分，有%d项'%len(df1 ))
        if len(df1)==0:return df_1
        idx=df1.index
        m1=std(df=df1)
        m1.tb()
        df1=m1.df

        df=self.df
        for i in df1.index:
            w=df1.loc[i]

            wb=w['路道街扩展']
            if wb is not None:
                dfx=df[df['路道街扩展']==wb].groupby('街道').size()
                if dfx.size!=0 :
                    df1.loc[i,'街道']=dfx.argmax() 
                    continue
            wa=w['楼群']
            if wa is not None:
                dfx=df[df['楼群']==wa].groupby('街道').size()
                if dfx.size!=0 :
                    df1.loc[i,'街道']=dfx.argmax()
                    continue
            wc=w['村社镇扩展']
            if wc is not None:
                dfx=df[df['村社镇扩展']==wc].groupby('街道').size()
                if dfx.size!=0:
                    df1.loc[i,'街道']=dfx.argmax() 
                    continue
            wc=w['村社镇']
            if wc is not None:
                dfx=df[df['村社镇']==wc].groupby('街道').size()
                if dfx.size!=0:
                    df1.loc[i,'街道']=dfx.argmax()
                    continue
        print('第二部分，完成')
        df_1.loc[idx,'word']=df1['街道'].values
        return df_1
    def p_write(self,name=None,sql=None):
        if name is None:name='dz_sist_jd'
        df=self.p_df(sql)
        print("开始写入")
        self.m.tomssql(df,'dz_sist_jd')


    def p_update(self,Udate='2017-05-01'):
        self._p_update_newEst(Udate)
        self._p_update_alterAddr(Udate)
    def _p_update_newEst(self,Udate):
        #后续的更新机制
        #Udate='2017-05-01'
        #找到新成立部分insert
        sql="""
        select  ztsfdm,jgdz from basedb.dbo.t_zzjgjz as t1 where ztsfdm is not null and jgdz is not null 
        and not exists (select 1 from test_dmyy.dbo.dz_sist_jd as t2 where t1.ztsfdm=t2.ztsfdm)
        and clrq>='%s'
        """%Udate
        df=self.p_df(sql)
        if not df.empty:
            print("开始写入,共计%d条"%len(df))
            df=df.where(df.notnull(),None)
            self.m.insert_sql("insert into test_dmyy.dbo.dz_sist_jd values(%s,%s,%s)",[tuple(x) for x in df.values])
            print("本次插入%d条新记录"%len(df))
       

        return df
    def _p_update_alterAddr(self,Udate):
         #更新做地址变更的部分
        #sql="""
        #with a as (
        #select * from (
        #SELECT entid ,alterdate,row_number() over (partition by entid order by alterdate desc) as rn FROM regdb.dbo.tdalteritem
        #where alteritemcode in('02','04','10') and alterdate>='2017-05-01') xx where rn=1)
        #select a.entid as ztsfdm,addr as jgdz from regdb.dbo.tdbase b ,a 
        #where b.entid=a.entid and b.authdate=a.alterdate
        #"""
        #改写成可以迁入with的形式
        #Udate='2017-05-01'
        sql="""
        select a.entid as ztsfdm,addr as jgdz from regdb.dbo.tdbase b ,

        (
        select * from (
        SELECT entid ,alterdate,row_number() over (partition by entid order by alterdate desc) as rn FROM regdb.dbo.tdalteritem
        where alteritemcode in('02','04','10') and alterdate>='%s') xx where rn=1) as a
        where b.entid=a.entid and b.authdate=a.alterdate
        """%Udate 
        df=self.p_df(sql)
        print("开始写dz_sist_jdAlterTmp,共%d行"%len(df))
        self.m.tomssql(df,'dz_sist_jdAlterTmp')
        sqlUpdate="""
        update test_dmyy.dbo.dz_sist_jd
        set word=t2.word,jgdz=t2.jgdz
        from test_dmyy.dbo.dz_sist_jd as t1,test_dmyy.dbo.dz_sist_jdAlterTmp as t2 
        where t1.ztsfdm=t2.ztsfdm
        """
        self.m.update_sql(sqlUpdate)






























"""
sql='''
select * from dz_std1
'''
#df=m.frommssql(sql)
path="F:\\work\\数据分析\\地理信息\\地址标准化\\df_zero.pkl"
#joblib.dump(df,path)
df=joblib.load(path)
print("df加载成功")
sql1='''
SELECT ztsfdm,jgdz from test_dmyy.dbo.dz_sist
where word is null and ztsfdm is not null
'''
m1=std(sql1)
m1.test()
df1=m1.df
#440300000052017032201801   深圳市宝安区47区和丰九巷1号301室 2017-03-22 00:00:00.000


for i in df1.index:
    w=df1.loc[i]

    wb=w['路道街扩展']
    if wb is not None:
        dfx=df[df['路道街扩展']==wb].groupby('街道').size()
        if dfx.size!=0 :
            df1.loc[i,'街道']=dfx.argmax() 
            continue
    wa=w['楼群']
    if wa is not None:
        dfx=df[df['楼群']==wa].groupby('街道').size()
        if dfx.size!=0 :
            df1.loc[i,'街道']=dfx.argmax()
            continue
    wc=w['村社镇扩展']
    if wc is not None:
        dfx=df[df['村社镇扩展']==wc].groupby('街道').size()
        if dfx.size!=0:
            df1.loc[i,'街道']=dfx.argmax() 
            continue
    wc=w['村社镇']
    if wc is not None:
        dfx=df[df['村社镇']==wc].groupby('街道').size()
        if dfx.size!=0:
            df1.loc[i,'街道']=dfx.argmax()
            continue
"""