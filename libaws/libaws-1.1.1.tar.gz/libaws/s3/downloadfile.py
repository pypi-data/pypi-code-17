#coding:utf-8
import os
import argparse
from libaws.common import config
from libaws.common.logger import enable_debug_log
from libaws.s3.download import manager
from libaws.s3 import daemonize

def main():
    parser = argparse.ArgumentParser()
    #指定下载的bucket,必须参数
    parser.add_argument("-b", "--bucket", type=str, dest="bucket",help='dest bucket to download file')
    #指定下载bucket中的文件,必须参数
    parser.add_argument("-k", "--key", type=str, dest="key", help = 'bucket file to download')
    #指定下载路径,默认为当前路径
    parser.add_argument("-p", "--path", type=str, dest="path", help = 'file download path to save',default = './',required=False)
    #指定下载文件名,默认和key一致
    parser.add_argument("-f", "--filename", type=str, dest="filename", help = 'download file name',default = None,required=False)
    #是否强制重新下载某个文件,默认为否
    parser.add_argument("-force", "--force-again-download", action='store_true', dest="force_again_download",help='need to download again when download is exists',default = False)
    parser.add_argument("-a", "--action", type=str, dest="action", help = 'start stop delete download',default = 'start')
    #是否开启日志调试模式
    parser.add_argument("-debug", "--enable-debug-log", action='store_true', dest="enable_debug_log",help='enable debug log or not',default = config.ENABLE_DEBUG_LOG)
    parser.add_argument("-d", "--daemon", action='store_true', dest="is_daemon_run",help='indicate this process is run in daemon or not',default = False)
    parser.add_argument("-t", "--thread", type=int, dest="thread_num",help='thread number to download file part',default=config.DEFAULT_THREAD_SIZE)
    args = parser.parse_args()
    bucket = args.bucket
    key = args.key
    
    filename = None
    if key is not None:
        filename = os.path.basename(key)
        if args.filename is not None:
            filename = args.filename

    dest_path = os.path.abspath(args.path)
    extra_args = {
        'force_again_download':args.force_again_download,
        'enable_debug_log':args.enable_debug_log,
        'thread_num':args.thread_num
    }
    if args.is_daemon_run:
        daemonize()
    download_config = config.DownloadConfig(bucket,key,dest_path,filename,**extra_args)
    enable_debug_log(args.enable_debug_log)
    download_manager = manager.DownloadManager(download_config)
    if bucket is not None and key is not None:
        dest_file = os.path.join(dest_path,filename)
        if args.action == 'start':
            download_manager.start_download(dest_file)
        elif args.action == 'stop':
            download_manager.stop_download()
        elif args.action == 'delete':
            download_manager.delete_download()
    else:
        if args.action == 'start':
            download_manager.start_all_download()
        elif args.action == 'stop':
            download_manager.stop_all_download()
        elif args.action == 'delete':
            download_manager.delete_all_download()

