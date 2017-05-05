import json
from qcloud_cos import *


def jsonify(data):
    return json.dumps(data, indent=4, ensure_ascii=False)


class QCloudCosTool(object):

    def __init__(self, config):
        self.check_config(config)
        self.bucket_name = config.pop('bucket_name')
        self.client = CosClient(**config)

    @staticmethod
    def check_config(config):
        for key, val in config.items():
            if not val:
                if key == 'appid':
                    export_key = 'QCOS_APPID'
                elif key == 'secret_id':
                    export_key = 'QCOS_SECRET_ID'
                elif key == 'secret_key':
                    export_key = 'QCOS_SECRET_KEY'
                elif key == 'region':
                    export_key = 'QCOS_REGION'
                elif key == 'bucket_name':
                    export_key = 'QCOS_BUCKET_NAME'
                raise AttributeError(
                    '{key} is not set, should export {export_key}=xxxxxx'.format(key=key, export_key=export_key))

    def get_bucket_info(self):
        pass

    def upload_file(self, local_file, remote_file=None, overwrite=1):
        remote_file = remote_file or '/' + local_file
        request = UploadFileRequest(self.bucket_name, remote_file.decode('utf-8'), local_file.decode('utf-8'),
                                    insert_only=overwrite)
        return jsonify(self.client.upload_file(request))

    def stat_file(self, remote_file):
        request = StatFileRequest(
            self.bucket_name, remote_file.decode('utf-8'))
        return jsonify(self.client.stat_file(request))

    def stat_folder(self, remote_folder):
        request = StatFolderRequest(
            self.bucket_name, remote_folder.decode('utf-8'))
        return jsonify(self.client.stat_folder(request))

    def update_file(self, remote_file, **kwargs):
        items = ['authority', 'biz_attr', 'cache_control', 'content_type']
        request = UpdateFileRequest(
            self.bucket_name, remote_file.decode('utf-8'))
        for item in items:
            if kwargs.get(item):
                if item == 'authority':
                    func = request.set_authority
                elif item == 'biz_attr':
                    func = request.set_biz_attr
                elif item == 'cache_control':
                    func = request.set_cache_control
                elif item == 'content_type':
                    func = request.set_content_type
                func(kwargs.get(item).decode('utf-8'))
        return jsonify(self.client.update_file(request))

    def del_file(self, remote_file):
        request = DelFileRequest(self.bucket_name, remote_file.decode('utf-8'))
        return jsonify(self.client.del_file(request))

    def create_folder(self, remote_folder):
        request = CreateFolderRequest(
            self.bucket_name, remote_folder.decode('utf-8'))
        return jsonify(self.client.create_folder(request))

    def update_folder(self, remote_folder, biz_attr):
        request = UpdateFolderRequest(
            self.bucket_name, remote_folder.decode('utf-8'))
        if biz_attr:
            request.set_biz_attr(biz_attr)
        return jsonify(self.client.update_folder(request))

    def list_folder(self, remote_folder, num=199):
        request = ListFolderRequest(
            self.bucket_name, remote_folder.decode('utf-8'), num)
        return jsonify(self.client.list_folder(request))

    def del_folder(self, remote_folder):
        request = DelFolderRequest(
            self.bucket_name, remote_folder.decode('utf-8'))
        return jsonify(self.client.del_folder(request))
