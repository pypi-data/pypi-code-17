from libaws.common.logger import logger
from libaws.s3.bucket import list_as_dir
from libaws.s3.download import download
from libaws.common.db import S3DownloadDb 

#获取下载数据库操作对象
s3_download_db = S3DownloadDb.get_db()

class DownloadManager(object):

    def __init__(self,download_config):
        self.download_config = download_config

    def start_download(self,dest_file):
        bucket,key = self.download_config.bucket,self.download_config.key
        logger.info('start download file %s',dest_file)
        if key.endswith("/"):
            total_file_count = 0
            total_success_count = 0
            total_fail_count = 0
            dir_keys = list_as_dir(bucket,key)
            for dkey in dir_keys:
                self.download_config.filename = dkey
                self.download_config.key = dkey
                download.start_download(self.download_config)
                total_file_count += 1
                if self.download_config.result:
                    total_success_count += 1
                else:
                    total_fail_count += 1
            logger.info("total download file count %d,success download count %d,fail download count %d",total_file_count,total_success_count,total_fail_count)
        else:
            download.start_download(self.download_config)
        logger.info('end download file %s',dest_file)

    def stop_download(self):
        download.stop_download(self.download_config)
        
    def delete_download(self):
        download.delete_download(self.download_config)

    def start_all_download(self):

        global s3_download_db
        results = s3_download_db.get_all_downloads()
        if 0 == len(results):
            logger.prompt("nothing to be download")
            return
        for result in results: 
            self.download_config.bucket = result[1] 
            self.download_config.key = result[2]
            self.download_config.dest_path = result[6]
            self.download_config.filename = result[4]
            dest_file = result[3]
            self.start_download(dest_file)

    def stop_all_download(self):

        global s3_download_db
        results = s3_download_db.get_all_downloads()
        if 0 == len(results):
            logger.prompt("nothing to be stop")
            return
        for result in results: 
            self.download_config.bucket = result[1] 
            self.download_config.key = result[2]
            self.download_config.dest_path = result[6]
            self.download_config.filename = result[4]
            self.stop_download()
        
    def delete_all_download(self):

        global s3_download_db
        results = s3_download_db.get_all_downloads()
        if 0 == len(results):
            logger.prompt("nothing to be delete")
            return
        for result in results: 
            self.download_config.bucket = result[1] 
            self.download_config.key = result[2]
            self.download_config.dest_path = result[6]
            self.download_config.filename = result[4]
            self.delete_download()

    
