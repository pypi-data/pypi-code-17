#coding:utf-8
import datetime
import os
import sys
import argparse
import Queue
from libaws.common.boto import *
from libaws.common.fileobj import *
from libaws.common.logger import *
from libaws.common.db import *
from libaws.common import utils,config,const
from libaws.base import callback,filerange
from libaws.common.errorcode import *
import partuploader

s3_upload_db = S3UploadDb.get_db()

def create_multipart_upload(bucket,dest_key):
    '''
        创建s3文件分块上传对象,返回一个随机唯一的upload_id
    '''

    response = client_s3.create_multipart_upload(Bucket=bucket,Key=dest_key)
    upload_id = response['UploadId']
    multi_part_upload = s3.MultipartUpload(bucket,dest_key,upload_id)

    return multi_part_upload

def create_upload_parts(multi_part_upload,part_num):
    '''
        创建s3上传分块对象列表
    '''
    
    if 1 >= part_num:
        return []

    multi_parts = []
    for i in range(part_num):
        part = multi_part_upload.Part(i + 1)
        multi_parts.append(part)

    return multi_parts


def sort_with_part_number(l,r):
    """
        按分块序号升序排序
    """
    p1 = l['PartNumber']
    p2 = r['PartNumber']

    if p1 > p2:
        return 1
    return -1

def save_file_info(file_obj):
    '''
        保存上传文件信息
    '''
    global s3_upload_db

    sql = '''
        INSERT INTO file(name,path,hash,time,size) VALUES (?, ?, ?,?,?)
    '''
    file_name,file_path,file_hash,file_date_time,file_size = file_obj.name,file_obj.path,\
                    file_obj.hash,file_obj.date_time,file_obj.size
    s3_upload_db.save(sql,[(file_name,file_path,file_hash,file_date_time,file_size),])

def store_multi_parts(file_obj,multi_parts,part_num,part_size):
    '''
        保存文件分块信息
    '''
    
    global s3_upload_db

    file_size = file_obj.size
    upload_id = file_obj.upload_id
    #分块个数
    #按分块个数对文件进行分割
    if part_num is not None:
        assert(part_num == len(multi_parts))
        file_ranges = filerange.get_file_ranges_by_part(file_obj.path,part_num,file_size)
    else:
        file_ranges = filerange.get_file_ranges_by_size(file_obj.path,part_size,file_size)

    datas = []
    for file_range in file_ranges:
        part_id = file_range.range_id
        block_size,start_byte,end_byte = file_range.size,file_range.start,file_range.end
        logger.debug('part_id:%d block_size:%ld,start_byte:%ld end_byte:%ld,is_last_block:%s',\
                        part_id,block_size,start_byte,end_byte,file_range.is_last)
        datas.append((part_id,block_size,start_byte,end_byte,upload_id,file_range.is_last))

    sql = '''
        insert into part (part_id,part_size,start_byte,end_byte,upload_id,is_last_part) values (?,?,?,?,?,?)
    '''
    s3_upload_db.save(sql,datas)

def create_multipart_upload_parts(file_obj,bucket,key,part_num,part_size):
    
    global s3_upload_db

    file_id = file_obj.file_id
    divide_part_num = None
    if part_num is None:
        part_num = filerange.get_part_num_by_size(file_obj.path,part_size,file_obj.size)
    else:
        divide_part_num = part_num

    multi_part_upload = create_multipart_upload(bucket,key)
    s3_upload_id = multi_part_upload.id

    sql = '''
        insert into upload(s3_upload_id,bucket,key,part_num,file_id,total_size,start_time,status) values(?,?,?,?,?,?,?,?) 
    '''

    now_time = datetime.datetime.now()
    s3_upload_db.save(sql,[(s3_upload_id,bucket,key,part_num,file_id,file_obj.size,now_time,const.STATUS_START_UPLOAD)])
    upload_parts = create_upload_parts(multi_part_upload,part_num)

    upload_id = s3_upload_db.get_upload_id(s3_upload_id)
    file_obj.upload_id = upload_id
    store_multi_parts(file_obj,upload_parts,divide_part_num,part_size)

def is_file_upload(file_obj,upload_id):
    '''
        查询文件是否已经成功上传过
    '''

    global s3_upload_db

    sql = '''
        select file_id,is_upload from upload where id=%d
    ''' % (upload_id)
    result = s3_upload_db.fetchone(sql)
    file_id,is_upload = result
    assert(file_id == file_obj.file_id)

    if is_upload:
        return True

    return False

def upload_file_multi_parts(file_obj,upload_id,callback=None):
    '''
        上传所有文件分块
    '''
    
    global s3_upload_db

    file_path,file_id = file_obj.path,file_obj.file_id

    #先在数据库里面查询该文件的上传分块信息
    sql = '''
        select file_id,s3_upload_id,part_num,bucket,key from upload where id=%d
    ''' % (upload_id)
    result = s3_upload_db.fetchone(sql)
    upload_file_id,s3_upload_id,part_num,bucket,dest_key = result
    assert(file_id == upload_file_id)

    sql = '''
        select * from part where upload_id=%d
    ''' % (upload_id)
    results = s3_upload_db.fetchall(sql)
    #分块个数不一致，报错
    if len(results) != part_num:
        logger.error('file:%s upload parts is damaged',file_path)
        return None,part_num,[] 
    
    multi_part_upload = s3.MultipartUpload(bucket,dest_key,s3_upload_id)
    part_ids = []
    #上传分块对象队列，采用多线程上传分块
    que = Queue.Queue()

    for row in results:
        multi_part_id = row[0]
        part_ids.append(multi_part_id)

        part_id = row[1]
        is_upload = row[5]
        block_size = row[2]

        start_time = row[8]
        if start_time is None:
            update_sql = '''
                update part set start_time=? where id=?
            '''
            now_time = datetime.datetime.now()
            data = [(now_time,multi_part_id),]
            s3_upload_db.update(update_sql,data)
        #分块已经上传成功，略过
        if is_upload:
            logger.info('file:%s part:%d has already uploaded',file_path,part_id)
            continue

        start_byte = row[3]
        end_byte = row[6]
        block_size = row[2]
        is_last_part = row[10]
        file_range = filerange.FileRange(file_path,part_id,start_byte,end_byte,block_size,is_last_part)
        multipart_upload_part = s3.MultipartUploadPart(bucket,dest_key,s3_upload_id,part_id)
        my_part_uploader = partuploader.MultiPartUploader(multi_part_id,multipart_upload_part,file_obj,file_range,callback)
        #将上传分块对象放入队列
        que.put(my_part_uploader)
    #启用多线程上传分块
    partuploader.MultiThreadUploader.start_upload_parts(que)
    return multi_part_upload,part_num,part_ids

def complete_multi_parts(file_obj,multi_part_upload,multi_part_ids,part_num):
    '''
        完成文件分块上传
    '''

    global s3_upload_db
    
    #判断分块个数是否一致
    if len(multi_part_ids) != part_num:
        return False

    parts = []
    upload_id = None

    md5s = []

    for upload_part_id in multi_part_ids:
        query_sql = '''
            select part_id,is_upload,etag,upload_id from part where id=%d
        ''' % (upload_part_id)

        result = s3_upload_db.fetchone(query_sql)
        if result is None:
            logger.error('part_id:%d has been deleted',upload_part_id)
            return False

        part_id,is_upload,etag,upload_id = result
        #判断分块是否上传成功，如果有一个未上传成功，则终止上传
        if not is_upload:
            logger.error('part_id:%d is not uploaded',upload_part_id)
            return False

        md5s.append(etag)
        #组合分块所需的分块的序号以及e_tag值
        part = {
            'PartNumber':part_id,
            'ETag':etag
        } 
   
        parts.append(part)
    s3_upload_db.set_upload_status(const.STATUS_UPLOAD_FINISHED,upload_id)
    #分块列表必须要按分块序号进行升序排序
    parts.sort(sort_with_part_number)
    try:
        #将所有分块组合成一个完整的文件，完成分块上传,返回最终文件的s3文件对象
        bucket,key,upload_id = multi_part_upload.bucket_name,multi_part_upload.object_key,multi_part_upload.id
        response = client_s3.complete_multipart_upload(Bucket=bucket,Key=key,UploadId=upload_id,
            MultipartUpload={
                'Parts':parts
        })
    except Exception,e:
        logger.error("%s",e)
        return False
    now_time = datetime.datetime.now()
    update_sql = '''
        update upload set is_upload=?,end_time=?,upload_percent=?,etag=?,status=? where id=?
    '''
    #获取上传文件的e_tag值
    file_obj.etag = response['ETag']
    #上传文件后校验上传文件是否正确
    if not file_obj.validate(md5s):
        s3_upload_db.set_upload_status(const.STATUS_UPLOAD_FAIL,file_obj.upload_id)
        logger.error("upload_id:%d md5 check sum is not match,etag is:%s",upload_id,utils.get_etag(md5s))
        return False

    logger.info("check upload file %s hash success",file_obj.path)
    s3_upload_db.update(update_sql,[(True,now_time,'100%',file_obj.etag,const.STATUS_UPLOAD_SUCCESS,file_obj.upload_id)])
    return True

def upload_small_file(file_obj,bucket,key):
    '''
        文件单块上传
    '''
    if 0 == file_obj.size:
        logger.warn("upload file %s size is 0",file_obj.path)

    transfer = S3Transfer(client_s3)
    file_path = file_obj.path
    
    s3_file_obj = s3.Object(bucket,key)
    err = False
    try:
        with callback.UploadProgressPercentage(file_path) as cb:
            s3_file_obj.upload_file(file_path,Callback=cb)
            logger.prompt("file %s upload to bucket %s success",file_path,bucket)
    except Exception,e:
        logger.debug(e)
        err = True

    return not err

def upload_file(upload_config):
    
    def init_upload_part():
        '''
            初始化上传信息
        '''
        save_file_info(file_obj)
        file_id = s3_upload_db.get_file_id_id_by_hash(file_obj.hash)
        file_obj.file_id = file_id
        create_multipart_upload_parts(file_obj,bucket,key,part_num,part_size)
        logger.info('create file %s multi upload parts success',file_obj.path)
        return file_id

    global s3_upload_db
    file_path,bucket,key,part_num,part_size = upload_config.file_path,upload_config.bucket,\
            upload_config.key,upload_config.part_number,upload_config.part_size
    #判断bucket是否存在
    try:
        if not utils.is_bucket_exists(bucket):
            logger.error("%s",ERROR_CODE_MESSAGES[BUCKET_NOT_EXISTS].format(bucket))
            return False
    except Exception,e:
        logger.error("%s",e)
        return False
        
    #判断本地文件是否存在
    if not os.path.exists(file_path):
        logger.error('file %s is not exists',file_path)
        return False

    file_obj = UploadFileObj(file_path)
    if key is None:
        key = file_obj.name
    
    #上传文件时，如果bucket上已经存在该文件，提示是否替换该文件
    if not upload_config.ignore_bucket_file and utils.is_bucket_file_exists(bucket,key):
        logger.warn("%s",ERROR_CODE_MESSAGES[BUCKET_UPLOAD_FILE_EXISTS].format(key,bucket))
        return False
    
    #文件大小小于默认分块上传的最小值时，使用单块上传方式
    if file_obj.size < config.DEFAULT_MULTI_UPLOAD_SIZE:
        return upload_small_file(file_obj,bucket,key)
    
    #通过文件hash值查找文件id
    file_id = s3_upload_db.get_file_id_id_by_hash(file_obj.hash)
    logger.info('get file %s hash success',file_obj.path)
    #第一次上传
    if not file_id:
        file_id = init_upload_part()
    else:
        file_obj.file_id = file_id
        if upload_config.force_again_upload:
            logger.debug('delete upload file_id:%d',file_id)
            s3_upload_db.delete_upload(file_id,bucket)
            file_id = init_upload_part()
    upload_id = s3_upload_db.get_upload_by_bucket_file(file_id,bucket)
    if not upload_id:
        create_multipart_upload_parts(file_obj,bucket,key,part_num,part_size)
        upload_id = s3_upload_db.get_upload_by_bucket_file(file_id,bucket)

    file_obj.upload_id = upload_id
    #文件已经上传过了
    if is_file_upload(file_obj,upload_id):
        #已经上传过的文件提示是否重新上传
        if not upload_config.force_again_upload:
            logger.warn('%s',ERROR_CODE_MESSAGES[UPLOAD_AGAIN_FILE_SUCCESS].format(file_obj.path,bucket))
            return False

    #开始上传所有分块 
    if config.LOGGER_DISABLED or not upload_config.enable_debug_log:
        upload_size = s3_upload_db.get_upload_size(file_obj.upload_id)
        part_upload_size = s3_upload_db.get_part_upload_size(file_obj.upload_id)
        logger.debug("total upload size %ld,total part upload size %ld",upload_size,part_upload_size)
        assert(part_upload_size == upload_size)
        with callback.UploadProgressPercentage(file_path,upload_size) as cb:
            multi_part_upload,part_num,part_ids = upload_file_multi_parts(file_obj,upload_id,callback=cb)
    else:
        multi_part_upload,part_num,part_ids = upload_file_multi_parts(file_obj,upload_id)

    if not multi_part_upload:
        return False
    
    logger.info('upload file %s multi parts success',file_obj.path)
    #将所有分块组合成一个最终的文件，并校验其hash值是否一致，完成此次上传
    if complete_multi_parts(file_obj,multi_part_upload,part_ids,part_num):
        logger.info("upload elapse time %s",s3_upload_db.get_upload_time(upload_id))
        return True
    else:
        return False

def start_upload(upload_config):

    file_path = upload_config.file_path
    if upload_file(upload_config):
        upload_config.result = True
        logger.prompt("upload file %s success",file_path)
    else:
        logger.error("upload file %s error",file_path)

