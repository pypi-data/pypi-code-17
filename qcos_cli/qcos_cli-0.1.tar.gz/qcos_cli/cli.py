import argparse
from qcos_cli.go import QCloudCosTool
from qcos_cli.config import config
from copy import deepcopy


def upload_file(args):
    if args.overwrite:
        overwrite = 0
    else:
        overwrite = 1
    print(QCloud.upload_file(args.local_file, args.remote_file, overwrite))


def stat_file(args):
    print(QCloud.stat_file(args.remote_file))


def update_file(args):
    attrs = deepcopy(args.__dict__)
    attrs.pop('func')
    attrs.pop('remote_file')
    print(QCloud.update_file(args.remote_file, **attrs))


def del_file(args):
    print(QCloud.del_file(args.remote_file))


def create_folder(args):
    print(QCloud.create_folder(args.remote_folder))


def update_folder(args):
    print(QCloud.update_folder(args.remote_folder, args.biz_attr))


def stat_folder(args):
    print(QCloud.stat_folder(args.remote_folder))


def list_folder(args):
    print(QCloud.list_folder(args.remote_folder, args.number))


def del_folder(args):
    print(QCloud.del_folder(args.remote_folder))


def get_parser():
    parser = argparse.ArgumentParser(prog='qcos_cli')
    sub = parser.add_subparsers()

    upload_file_parser = sub.add_parser(
        'upload_file', help='upload local file')
    upload_file_parser.add_argument('local_file', help='local file path')
    upload_file_parser.add_argument(
        'remote_file', help='remote file path, start with /, end not /')
    upload_file_parser.add_argument(
        '--overwrite', action='store_true', default=False, help='overwrite remote file')
    upload_file_parser.set_defaults(func=upload_file)

    stat_file_parser = sub.add_parser(
        'stat_file', help='show remote file status')
    stat_file_parser.add_argument(
        'remote_file', help='remote file path, start with /, end not /')
    stat_file_parser.set_defaults(func=stat_file)

    update_file_parser = sub.add_parser('update_file', help='update file')
    update_file_parser.add_argument(
        'remote_file', help='remote file path, start with /, end not /')
    update_file_parser.add_argument(
        '--biz_attr', default=None, help='update file attr')
    update_file_parser.add_argument(
        '--authority', default=None, help='update file authority')
    update_file_parser.add_argument(
        '--cache_control', default=None, help='update cache control header')
    update_file_parser.add_argument(
        '--content_type', default=None, help='update content type header')
    update_file_parser.set_defaults(func=update_file)

    del_file_parser = sub.add_parser('del_file', help='del file')
    del_file_parser.add_argument(
        'remote_file', help='remote file path, start with /, end not /')
    del_file_parser.set_defaults(func=del_file)

    create_folder_parser = sub.add_parser(
        'create_folder', help='create folder')
    create_folder_parser.add_argument(
        'remote_folder', help='remote folder path, start with /, end must /')
    create_folder_parser.set_defaults(func=create_folder)

    update_folder_parser = sub.add_parser(
        'update_folder', help='update folder')
    update_folder_parser.add_argument(
        'remote_folder', help='remote folder path, start with /, end must /')
    update_folder_parser.add_argument(
        '--biz_attr', default=None, help='update folder attr')
    update_folder_parser.set_defaults(func=update_folder)

    stat_folder_parser = sub.add_parser(
        'stat_folder', help='show remote folder status')
    stat_folder_parser.add_argument(
        'remote_folder', help='remote folder path, start with /, end must /')
    stat_folder_parser.set_defaults(func=stat_folder)

    del_folder_parser = sub.add_parser('del_folder', help='del folder')
    del_folder_parser.add_argument(
        'remote_folder', help='del folder path, start with /, end must /')
    del_folder_parser.set_defaults(func=del_folder)

    list_folder_parser = sub.add_parser('list_folder', help='list folder')
    list_folder_parser.add_argument(
        'remote_folder', help='remote folder path, start with /, end must /')
    list_folder_parser.add_argument('--number', help='list file number')
    list_folder_parser.set_defaults(func=list_folder)

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    global QCloud
    QCloud = QCloudCosTool(config)
    args.func(args)
