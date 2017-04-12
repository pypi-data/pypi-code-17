#coding:utf-8
import os
import base64
from boto import *
from libaws.base import platform,md5

def get_format_tag(etag):
    '''
        将s3上的文件e_tag值去除前后的引号(")
    '''

    strip_etag = etag.lstrip('"').rstrip('"')
    return strip_etag

def get_etag(md5s):
    ''' s3上计算分块上传文件的e_tag算法 将所有分块的md5值汇总，转换大写，计算base64值，再获取base64内容的md5值
    '''

    md5str = ''.join(md5s)
    upper_md5str = md5str.upper()
    b64 = base64.b16decode(upper_md5str)
    b64_md5 = md5.get_str_md5(b64)
	
    etag = b64_md5 + "-" + str(len(md5s))
    return etag


def split_etag(etag):

    strip_etag = get_format_tag(etag)
    lsts = strip_etag.split('-')

    md5_str = lsts[0]
    part_number = int(lst[1])

    return md5_str,part_number


def is_bucket_file_exists(bucket,key):
    '''
        判断bucket里面的文件是否存在
        不存在的文件没有e_tag值，会抛出异常
    '''
    try:
        s3_file_obj = s3.Object(bucket,key)
        etag = s3_file_obj.e_tag
        return True
    except botocore.exceptions.ClientError,e:
        return False

def is_bucket_exists(bucket):
    '''
        判断bucket是否存在
    '''

    s3_bucket = s3.Bucket(bucket)
    try:
        s3_bucket = s3.Bucket(bucket)
        s3_bucket.wait_until_exists()
        return True
    except botocore.exceptions.ClientError,e:
        if str(e).find('(404)') != -1:
            return False
    except botocore.exceptions.WaiterError,e:
        return False

def get_app_data_path():

    if platform.CURRENT_OS_SYSTEM == platform.WINDOWS_OS_SYSTEM:

        base_app_data_path = os.getenv('APPDATA','.')
        app_data_path = os.path.join(base_app_data_path,'.libaws')
    elif platform.CURRENT_OS_SYSTEM == platform.LINUX_OS_SYSTEM:

        base_app_data_path = os.getenv('HOME','.')
        app_data_path = os.path.join(base_app_data_path,'.libaws')
    
    return app_data_path

def get_region():

    aws_region_keyword =  'AWS_DEFAULT_REGION'
    home_dir = os.environ['HOME']
    region_file_name = '%s/.aws/config' % (home_dir)
    region = None
    
    if os.path.exists(region_file_name):
        import ConfigParser
        config = ConfigParser.ConfigParser()
        with open(region_file_name) as f2:
            config.readfp(f2)
            region = config.get("default",'region')

    if os.environ.has_key(aws_region_keyword):
        environ = os.environ
        region = environ[aws_region_keyword]

    return region

def get_file_hash(file_path):

    from fileobj import FileObj
    file_path = os.path.abspath(file_path)
    file_obj = FileObj(file_path)
    return file_obj.get_hash()

def get_file_hash_by_part(file_path,part_number):

    from fileobj import FileObj
    file_path = os.path.abspath(file_path)
    file_obj = FileObj(file_path)
    file_obj.size = os.path.getsize(file_path)

    md5s = file_obj.get_file_range_md5s_by_part(part_number)
    return get_etag(md5s)

def get_file_hash_by_size(file_path,part_size):

    from fileobj import FileObj
    file_path = os.path.abspath(file_path)
    file_obj = FileObj(file_path)
    file_obj.size = os.path.getsize(file_path)

    md5s = file_obj.get_file_range_md5s_by_size(part_size*1024**2)
    return get_etag(md5s)

