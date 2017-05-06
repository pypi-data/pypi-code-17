import fire
from qcos_cli.go import QCloudCosTool

QCloud = QCloudCosTool()


class FileOps(object):
    @staticmethod
    def upload(local_file, remote_file, overwrite=False):
        if overwrite:
            overwrite = 0
        else:
            overwrite = 1
        return QCloud.upload_file(local_file, remote_file, overwrite)

    @staticmethod
    def stat(remote_file):
        return QCloud.stat_file(remote_file)

    @staticmethod
    def update(remote_file, authority=None, biz_attr=None, cache_control=None, content_type=None):
        attrs = {'authority': authority,
                 'biz_attr': biz_attr,
                 'cache_control': cache_control,
                 'content_type': content_type}
        return QCloud.update_file(remote_file, **attrs)

    @staticmethod
    def delete(remote_file):
        return QCloud.del_file(remote_file)


class FolderOps(object):
    @staticmethod
    def create(remote_folder):
        return QCloud.create_folder(remote_folder)

    @staticmethod
    def update(remote_folder, biz_attr=None):
        return QCloud.update_folder(remote_folder, biz_attr)

    @staticmethod
    def list(remote_folder, num=199):
        return QCloud.list_folder(remote_folder, num)

    @staticmethod
    def delete(remote_folder):
        return QCloud.del_folder(remote_folder)


class Pipeline(object):
    def __init__(self):
        self.file = FileOps()
        self.folder = FolderOps()


def main():
    fire.Fire(Pipeline)
