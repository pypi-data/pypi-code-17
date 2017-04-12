#coding:utf-8
import argparse
import os
from libaws.common import config
from libaws.common.logger import logger,enable_debug_log
from libaws.s3.upload import upload
from libaws.s3 import daemonize



def iter_path(path):
    for home,dirs,files in os.walk(path):
        for filename in files:
            yield os.path.join(home, filename)

def main():
    parser = argparse.ArgumentParser()
    #上传文件路径，必须参数
    parser.add_argument("-p", "--path", type=str, dest="file_path", required=True)
    #上传至的bucket,必须参数
    parser.add_argument("-b", "--bucket", type=str, dest="bucket",help='dest bucket to upload',required=True)
    #上传分块个数，默认为6
    parser.add_argument("-n", "--num", type=int, dest="part_num",help='part num of file')
    parser.add_argument("-z", "--size", type=int, dest="part_size",help='part size of file',default=config.DEFAULT_UPLOAD_PART_SIZE)
    #上传至bucket的文件名,默认为上传文件名
    parser.add_argument("-k", "--key", type=str, help="dest bucket key",dest='key',default=None)
    #bucket存在和上传文件名一致的时候是否替换目的文件
    parser.add_argument("-i", "--ignore-bucket-file", action='store_true', dest="ignore_bucket_file",help='when file exist in bucket ,ignore it or not',default=False)
    #是否强制重新上传某个文件
    parser.add_argument("-force", "--force-again-upload", action='store_true', dest="force_again_upload",help='need to upload again when upload is exists',default = False)
    #进程是否后台运行
    parser.add_argument("-d", "--daemon", action='store_true', dest="is_daemon_run",help='indicate this process is run in daemon or not',default = False)
    #是否开启日志调试模式
    parser.add_argument("-debug", "--enable-debug-log", action='store_true', dest="enable_debug_log",help='enable debug log or not',default = config.ENABLE_DEBUG_LOG)
    parser.add_argument("-t", "--thread", type=int, dest="thread_num",help='thread number to upload file part',default=config.DEFAULT_THREAD_SIZE)
    args = parser.parse_args()
    file_path = args.file_path
    bucket = args.bucket
    key = args.key
    part_num = args.part_num
    part_size = args.part_size
    extra_args = {
        'ignore_bucket_file':args.ignore_bucket_file,
        'force_again_upload':args.force_again_upload,
        'is_daemon_run':args.is_daemon_run,
        'enable_debug_log':args.enable_debug_log
    }


    config.DEFAULT_THREAD_SIZE = args.thread_num
    file_path = os.path.abspath(file_path)
    upload_config = config.UploadConfig(bucket,key,file_path,part_num,part_size,**extra_args)

    #设置调试日志
    enable_debug_log(args.enable_debug_log)
    #设置进程后台运行
    if args.is_daemon_run:
        daemonize()
    logger.info('start upload file %s',(file_path))
    if os.path.isdir(file_path):
        total_file_count = 0
        total_success_count = 0
        total_fail_count = 0
        if not file_path.endswith("/"):
            file_path += "/"
        for child_file_path in iter_path(file_path):
            upload_config.file_path = child_file_path 
            upload_config.key = child_file_path.replace(file_path,"")
            if key is not None:
                upload_config.key = os.path.join(key,upload_config.key)
            upload.start_upload(upload_config)
            total_file_count += 1
            if upload_config.result:
                total_success_count += 1
            else:
                total_fail_count += 1
        logger.info("total upload file count %d,success upload count %d,fail upload count %d",total_file_count,total_success_count,total_fail_count)
    else:
        upload.start_upload(upload_config)
    logger.info('end upload file %s',(file_path))

if __name__== "__main__":
    main()

