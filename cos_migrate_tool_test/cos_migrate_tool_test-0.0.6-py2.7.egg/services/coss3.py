# -*- coding: utf-8 -*

from logging import getLogger
from migrate_tool import storage_service
from coscmd.client import CosS3Client, CosConfig

from migrate_tool.task import Task

def to_unicode(s):
    if isinstance(s, str):
        return s.decode('utf-8')
    else:
        return s


def to_utf8(s):
    if isinstance(s, unicode):
        return s.encode('utf-8')
    else:
        return s


logger = getLogger(__name__)

class CosS3StorageService(storage_service.StorageService):

    def __init__(self, *args, **kwargs):

        appid = int(kwargs['appid'])
        region = kwargs['region']
        accesskeyid = unicode(kwargs['accesskeyid'])
        accesskeysecret = unicode(kwargs['accesskeysecret'])
        bucket = unicode(kwargs['bucket'])
        if 'prefix_dir' in kwargs:
            self._prefix_dir = kwargs['prefix_dir']
        else:
            self._prefix_dir = None

        if 'part_size' in kwargs:
            self._part_size = kwargs['part_size']
        else:
            self._part_size = 1

        conf = CosConfig(appid=appid, access_id=accesskeyid, access_key=accesskeysecret, region=region, bucket=bucket,                         part_size=self._part_size)
        self._cos_client = CosS3Client(conf)
        self._bucket = bucket
        self._overwrite = kwargs['overwrite'] == 'true' if 'overwrite' in kwargs else False
        self._max_retry = 20

    def download(self, task, local_path):
        # self._oss_api.get_object_to_file(urllib.unquote(cos_path).encode('utf-8'), local_path)
        raise NotImplementedError

    def upload(self, task, local_path):
        cos_path = task.key
        if not cos_path.startswith('/'):
            cos_path = '/' + cos_path

        if self._prefix_dir:
            cos_path = self._prefix_dir + cos_path

        if isinstance(local_path, unicode):
            local_path.encode('utf-8')
        if cos_path.startswith('/'):
            cos_path = cos_path[1:]

        insert_only = 0 if self._overwrite else 1
        mp = selt._cos_client.multipart_upload_from_filename(local_path, cos_path)
        for i in range(10):
            rt = mp.init_mp() 
            if rt:
                break
            logger.warn("init multipart upload failed")
        else:
            raise IOError("upload failed")
                
        for i in range(10):
            rt = mp.upload_parts()
            if rt:
                break
            logger.warn("multipart upload part failed")
        else:
            raise IOError("upload failed")
                    
        for i in range(10):
            rt = mp.complete_mp()
            if rt:
                break
            logger.warn("finish upload part failed")
        else:
            raise IOError("upload failed")

    def list(self):
         raise NotImplementedError

    def exists(self, task):
        return False
