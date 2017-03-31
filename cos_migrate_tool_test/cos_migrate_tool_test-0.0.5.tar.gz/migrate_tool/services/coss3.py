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

    def dfs(self, path):
        print "DFS: {path}".format(path=to_utf8(path))
        _finish = False
        _context = u''
        max_retry = self._max_retry

        path = to_unicode(path)

        while not _finish:
            request = ListFolderRequest(bucket_name=self._bucket, cos_path=path, context=_context)
            ret = self._cos_api.list_folder(request)

            if ret['code'] != 0:
                max_retry -= 1
            else:
                _finish = ret['data']['listover']
                _context = ret['data']['context']
                for item in ret['data']['infos']:
                    if 'filelen' in item:
                        try:
                            key = "{prefix}{filename}".format(prefix=path, filename=item['name'])
                            yield Task(key, item['filelen'], None)
                        except:
                            pass
                    else:
                        _sub_dir = "{prefix}{filename}".format(prefix=path.encode('utf-8'),
                                                               filename=item['name'].encode('utf-8'))
                        for i in self.dfs(_sub_dir):
                            yield i

            if max_retry == 0:
                _finish = True

    def exists(self, task):
        _path = task.key
        _size = task.size

        if not _path.startswith('/'):
            _path = '/' + _path
        logger = getLogger(__name__)
        # logger.info("func: exists: " + str(_path))
        if self._prefix_dir:
            _path = self._prefix_dir + _path

        if isinstance(_path, str):
            _path = _path.decode('utf-8')
        request = StatFileRequest(self._bucket, _path)
        ret = self._cos_api.stat_file(request)
        logger.debug("ret: " + str(ret))
        # import json
        # v = json.loads(ret)
        if ret['code'] != 0:
            # logger.warn("error code: " + str(ret['code']))
            return False
        if ret['data']['filelen'] != ret['data']['filesize']:
            logger.warn("file is broken, filelen: {len}, filesize: {size}".format(
                len=ret['data']['filelen'],
                size=ret['data']['filesize']
            ))
            return False
        elif _size is not None and ret['data']['filelen'] != _size:
            return False
        elif ret['data']['filelen'] != _size:
            return False
        return True
