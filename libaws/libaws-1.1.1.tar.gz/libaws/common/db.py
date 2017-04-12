#coding:utf-8
import os
import config
import sql
from libaws.common.logger import *
from libaws.base import singleton
from libaws.base.basedb import *
from boto import ec2,client_s3
import libaws.base.utils as baseutils
import utils
import datetime

def init_db_path():
    try:
        app_data_path = utils.get_app_data_path()
        db_data_path = os.path.join(app_data_path,'data')
        baseutils.mkdirs(db_data_path)
    except Exception,e:
        print e
        db_data_path = "./.libaws/data"
        baseutils.mkdirs(db_data_path)

    return db_data_path

class S3UploadDb(BaseDb):

    '''
        上传文件数据库类
    '''
    #设置该类是单例
    __metaclass__ = singleton.Singleton

    def __init__(self):
        
        db_dir = init_db_path()
        db_path = os.path.join(db_dir,config.UPLOAD_DB_NAME)

        super(S3UploadDb,self).__init__(db_path)
        self.init_upload_db()

    @classmethod
    def get_db(cls):
        return S3UploadDb()

    def init_upload_db(self):

        table_already_exist_flag = 'already exists'

        #创建upload表，表存在时不抛异常
        try:
            self.create_table(sql.CREATE_UPLOAD_TABLE_SQL,config.UPLOAD_TABLE)
            logger.info('create table %s success',config.UPLOAD_TABLE)
        except sqlite3.OperationalError,e:
            if str(e).find(table_already_exist_flag) == -1:
                print e
                return 

        #创建part表，表存在时不抛异常
        try:
            self.create_table(sql.CREATE_PART_TABLE_SQL,config.UPLOAD_PART_TABLE)
            logger.info('create table %s success',config.UPLOAD_PART_TABLE)
        except sqlite3.OperationalError,e:
            if str(e).find(table_already_exist_flag) == -1:
                print e
                return 

        #创建file表，表存在时不抛异常
        try:
            self.create_table(sql.CREATE_FILE_TABLE_SQL,config.UPLOAD_FILE_TABLE)
            logger.info('create table %s success',config.UPLOAD_FILE_TABLE)
        except sqlite3.OperationalError,e:
            if str(e).find(table_already_exist_flag) == -1:
                print e
                return 

    def get_file_id_id_by_hash(self,file_hash):
        '''
            通过文件hash值获取文件id
        '''
        query_sql = '''
                select id from file where hash='%s'
            ''' % (file_hash)

        result = self.fetchone(query_sql)
        if not result:
            return None
        return result[0]
    
    def get_upload_id(self,s3_upload_id):
        '''
            通过s3上的upload_id获取数据库里面自增的upload_id
        '''
        query_sql = '''
            select id from upload where s3_upload_id='%s'
        ''' % (s3_upload_id)

        result = self.fetchone(query_sql)
        if not result:
            return None
        return result[0]
  
    def get_upload_by_bucket_file(self,file_id,bucket):
        '''
            通过文件id获取上传id
        '''
        query_sql = '''
            select id from upload where file_id=%d and bucket='%s'
        ''' % (file_id,bucket)

        result = self.fetchone(query_sql)
        if not result:
            return None
        return result[0]

    def get_upload_size(self,upload_id):
        
        query_sql = '''
            select upload_size from upload where id=%d
        ''' % (upload_id)

        result = self.fetchone(query_sql)
        return result[0]

    def get_part_upload_size(self,upload_id):

        query_sql = '''
            select part_size from part where upload_id=%d and is_upload=1
        ''' % (upload_id)
        results = self.fetchall(query_sql)
        upload_size = 0
        for result in results:
            upload_size += result[0]

        return upload_size

    def delete_upload(self,file_id,bucket):
        '''
            删除该上传相关联的所有表
        '''
        #delete_sql = '''
         #   delete from file where id=%d
        #''' % (file_id)
        #self.delete(delete_sql)
        upload_id = self.get_upload_by_bucket_file(file_id,bucket)

        #删除上传信息时，删除s3上保留的分块信息
        query_sql = '''
            select bucket,key,s3_upload_id from upload where id=%d
        ''' % (upload_id)
        bucket,key,s3_upload_id = self.fetchone(query_sql)
        try:
            client_s3.abort_multipart_upload(
                Bucket=bucket,Key=key,UploadId=s3_upload_id,
            )
        except Exception,e:
            logger.warn("%s",e)

        delete_sql = '''
            delete from part where upload_id=%d
        ''' % (upload_id)
        self.delete(delete_sql)

        delete_sql = '''
            delete from upload where file_id=%d
        ''' % (file_id)
        self.delete(delete_sql)
    
    def set_upload_status(self,status,upload_id):

        update_sql = '''
            update upload set status=%d where id=%d
        ''' % (status,upload_id)

        self.update(update_sql)

    def get_upload_time(self,upload_id):

        query_sql = '''
            select start_time,end_time from upload where id=%d
        ''' % (upload_id)

        result = self.fetchone(query_sql)
        str_start_time = result[0][0:result[0].find(".")]
        str_end_time = result[1][0:result[1].find(".")]

        start_time = datetime.datetime.strptime(str_start_time,"%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(str_end_time,"%Y-%m-%d %H:%M:%S")

        time_delta = end_time - start_time
        time_delta_second = time_delta.seconds

        if time_delta_second < 60:
            return "%d S" % (time_delta_second)
        elif time_delta_second < 60 * 60:
            return "%.1f M" % (time_delta_second/60.0)
        else:
            return "%.1f H" % (time_delta_second/60.0/60.0)


class S3DownloadDb(BaseDb):
    '''
        下载文件数据库类
    '''

    #表示该类是单例类
    __metaclass__ = singleton.Singleton

    def __init__(self):
        
        db_dir = init_db_path()
        db_path = os.path.join(db_dir,config.DOWNLOAD_DB_NAME)
        super(S3DownloadDb,self).__init__(db_path)
        self.init_download_db()

    @classmethod
    def get_db(cls):
        return S3DownloadDb()

    def init_download_db(self):

        table_already_exist_flag = 'already exists'

        #创建download表，表存在时不抛异常
        try:
            self.create_table(sql.CREATE_DOWNLOAD_TABLE_SQL,config.DOWNLOAD_TABLE)
            logger.info('create table %s success',config.DOWNLOAD_TABLE)
        except sqlite3.OperationalError,e:
            if str(e).find(table_already_exist_flag) == -1:
                print e
                return 

        #创建range表，表存在时不抛异常
        try:
            self.create_table(sql.CREATE_DOWNLOAD_RNAGE_TABLE_SQL,config.DOWNLOAD_RANGE_TABLE)
            logger.info('create table %s success',config.DOWNLOAD_RANGE_TABLE)
        except sqlite3.OperationalError,e:
            if str(e).find(table_already_exist_flag) == -1:
                print e
                return 

    def get_download_id(self,bucket,key):

        query_sql = '''
            select id from download where bucket=? and key=?
        ''' 

        data = (bucket,key)
        result = self.fetchone(query_sql,data)
        if not result:
            return None
        return result[0]
    
    def get_all_downloads(self):

        query_sql = '''
            select * from download 
        ''' 
        return self.fetchall(query_sql)
    
    def get_download_info(self,id):

        query_sql = '''
            select download_size,tmp_file_path,is_download from download where id=%d
        ''' % (id)
        result = self.fetchone(query_sql)
        return result
    
    def delete_download(self,id):
        '''
            删除该下载相关联的所有表
        '''
        
        query_sql = '''
            select tmp_file_path from download where id=%d
        ''' % (id)
        tmp_file_path = self.fetchone(query_sql)[0]
        #重新下载时，删除上次下载产生的临时文件
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)

        delete_sql = '''
            delete from download where id=%d
        ''' % (id)
        self.delete(delete_sql)
       
        delete_sql = '''
            delete from range where download_id=%d
        ''' % (id)
        self.delete(delete_sql)

    def get_download_size(self,download_id):
        
        query_sql = '''
            select download_size from download where id=%d
        ''' % (download_id)

        result = self.fetchone(query_sql)
        return result[0]

    def get_total_range_download_size(self,download_id):
                
        query_sql = '''
            select download_size from range where download_id=%d
        ''' % (download_id)

        results = self.fetchall(query_sql)
        download_size = 0
        for result in results:
            download_size += result[0]
        return download_size
    
    def reset_download_size(self,download_size,download_id):

        update_sql = '''
            update download set download_size=%d where id=%d
        ''' % (download_size,download_id)

        self.update(update_sql)

    def get_download_status(self,download_id):
        
        query_sql = '''
            select status from download where id=%d
        ''' % (download_id)

        result = self.fetchone(query_sql)
        return result[0]

    def set_download_status(self,status,download_id):

        update_sql = '''
            update download set status=%d where id=%d
        ''' % (status,download_id)

        self.update(update_sql)
    
    def get_range_number(self,download_id):
        
        query_sql = '''
            select range_num from download where id=%d
        ''' % (download_id)

        result = self.fetchone(query_sql)
        return result[0]
  
    def get_range_download_size(self,range_id):
        
        query_sql = '''
            select download_size from range where id=%d
        ''' % (range_id)

        result = self.fetchone(query_sql)
        return result[0]
    
    def is_range_finished(self,range_id):
            
        query_sql = '''
            select is_download from range where id=%d
        ''' % (range_id)

        result = self.fetchone(query_sql)
        return result[0]
    
    def get_download_time(self,download_id):

        query_sql = '''
            select start_time,end_time from download where id=%d
        ''' % (download_id)

        result = self.fetchone(query_sql)
        str_start_time = result[0][0:result[0].find(".")]
        str_end_time = result[1][0:result[1].find(".")]

        start_time = datetime.datetime.strptime(str_start_time,"%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(str_end_time,"%Y-%m-%d %H:%M:%S")

        time_delta = end_time - start_time
        time_delta_second = time_delta.seconds

        if time_delta_second < 60:
            return "%d S" % (time_delta_second)
        elif time_delta_second < 60 * 60:
            return "%.1f M" % (time_delta_second/60.0)
        else:
            return "%.1f H" % (time_delta_second/60.0/60.0)
  
    def get_range_id(self,range_id):
                
        query_sql = '''
            select range_id from range where id=%d
        ''' % (range_id)
        result = self.fetchone(query_sql)
        return result[0]

    def get_range_size(self,range_id):
                
        query_sql = '''
            select range_size from range where id=%d
        ''' % (range_id)
        result = self.fetchone(query_sql)
        return result[0]

class Ec2InstanceDb(BaseDb):
    '''
    '''

    #表示该类是单例类
    __metaclass__ = singleton.Singleton

    def __init__(self):
        
        db_dir = init_db_path()
        db_path = os.path.join(db_dir,config.DEFAULT_INSTANCE_CONFIG_DB_NAME)
        super(Ec2InstanceDb,self).__init__(db_path)
        self.init_instance_db()

    @classmethod
    def get_db(cls):
        return Ec2InstanceDb()

    def init_instance_db(self):

        table_already_exist_flag = 'already exists'

        try:
            self.create_table(sql.CREATE_INSTANCE_TABLE_SQL,config.DEFAULT_INSTANCE_CONFIG_TABLE_NAME)
            logger.info('create table %s success',config.DEFAULT_INSTANCE_CONFIG_TABLE_NAME)
        except sqlite3.OperationalError,e:
            if str(e).find(table_already_exist_flag) == -1:
                print e
                return 
    
    def delete_all_network_config(self):

        query_sql = '''
            select vpc_id subnet_id,keyname,security_group_id,image_id,key_path from instance 
        '''
        for result in self.fetchall(query_sql):
            vpc_id = result[0]
            try:
                vpc = ec2.Vpc(vpc_id)
                gateway = list(vpc.internet_gateways.all())[0]
                gateway.detach_from_vpc(VpcId=vpc_id)
                gateway.delete()
   
                #route_table = list(vpc.route_tables.all())[0]
                #routetable_associationid = route_table.associations_attribute[0]['RouteTableAssociationId']
                #route_table_association = ec2.RouteTableAssociation(routetable_associationid)
                #route_table_association.delete()
                #route_table.delete()
         
                subnet = list(vpc.subnets.all())[0]
                subnet.delete()
            
                security_group = list(vpc.security_groups.all())[1]
                security_group.delete()

                vpc.delete()
            except Exception,e:
                logger.warn("%s",e)
                logger.warn("delete vpc %s fail",vpc_id)

    def save_instance_info(self,instance_id,tag,image_id,keyname,security_group_id,subnet_id,pem_file_path,vpc_id,instance_type):

        insert_sql = '''
            insert into instance(instance_id,tag,keyname,subnet_id,image_id,security_group_id,key_path,vpc_id,region,type) values(?,?,?,?,?,?,?,?,?,?)
        '''
        region = utils.get_region()
        data = [(instance_id,tag,keyname,subnet_id,image_id,security_group_id,pem_file_path,vpc_id,region,instance_type),]
        self.save(insert_sql,data)


    def delete_instance_info(self,instance_id):

        sql = '''
            delete from instance where instance_id='%s'
        ''' % (instance_id)
        self.delete(sql)

    def get_instance_by_tag(self,tag):
        query_sql = '''
            select * from instance 
        '''
        results = self.fetchall(query_sql)
        instance_info = []
        for result in results:
            if result[4].find(tag) != -1:
                d = {}
                d['instance_id'] = result[1]
                d['tag'] = result[4]
                d['type'] = result[2]
                d['region'] = result[10]
                d['create_time'] = result[11]
                instance_info.append((result[1],result[4],result[2],result[10],result[11]),)
        return instance_info

    def load_default_config(self):

        region = utils.get_region()
        query_sql = '''
            select subnet_id,keyname,security_group_id,image_id,key_path from instance where region="%s" 
        '''% (region,)
        return self.fetchone(query_sql)
