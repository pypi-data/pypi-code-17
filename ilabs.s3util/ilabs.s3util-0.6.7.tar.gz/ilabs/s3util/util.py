import glob
import html
import os
import configparser
import re
import boto3
import botocore
import io
from types import SimpleNamespace
import sys


def cli_pypi(args):

    prepared_files = list(prepare(args.file_mask))
    if not prepared_files:
        raise RuntimeError('No files to upload')

    target = args.target or find_from_pip_conf()
    if target is None:
        raise RuntimeError('Could not find target bucket and prefix names. Use "target" option to specify them explicitly, e.g. target=s3://my_bucket/my_prefix')

    bucket, prefix = parse_target(target)

    s3 = boto3.resource('s3',
            aws_access_key_id=args.aws_access_key_id,
            aws_secret_access_key=args.aws_secret_access_key)

    packages = set()
    for x in prepared_files:
        package = package_from_name(x.name)
        x.key = package + '/' + x.name
        if prefix is not None:
            x.key = prefix + '/' + x.key
        packages.add(package)

        if not args.force and key_exists(s3, bucket, x.key):
            raise RuntimeError('Key %s already exists. Use "force" option to force file overwrite' % (package + '/' + x.name))

    for x in prepared_files:
        obj = s3.Object(bucket, x.key)
        upload_object(x.fname, obj, ACL='public-read')

    for package in sorted(packages):
        key = prefix + '/' + package if prefix is not None else package
        public_files = list_public_files(s3, bucket, key)

        body = '\n'.join(TEMPLATE_LINE.format(
            name=html.escape(name)) for name in public_files if not name.endswith('index.html'))
        text = TEMPLATE.format(body=body)

        print('Creating index for package %s' % package)
        s3.Object(bucket, key + '/index.html').put(
            Body=text.encode(),
            ContentType='text/html',
            CacheControl='public, must-revalidate, proxy-revalidate, max-age=0',
            ACL='public-read'
        )

def cli_upload(args):

    prepared_files = list(prepare(args.file_mask))
    if not prepared_files:
        raise RuntimeError('No files to upload')

    if args.target is None:
        raise RuntimeError('Required parameter "target" is missing')

    bucket, prefix = parse_target(args.target)

    s3 = boto3.resource('s3',
            aws_access_key_id=args.aws_access_key_id,
            aws_secret_access_key=args.aws_secret_access_key)

    for x in prepared_files:
        x.key = x.name if prefix is None else prefix + '/' + x.name
        if not args.force and key_exists(s3, bucket, x.key):
            raise RuntimeError('File %s already exists. Use "force" option to force file overwrite' % x.name)

    for x in prepared_files:
        obj = s3.Object(bucket, x.key)
        upload_object(x.fname, obj, ACL=args.acl)

def upload_object(fname, obj, **options):
    assert 'Body' not in options

    options = dict(options)

    acl = options.pop('ACL', 'private')
    mime = options.pop('ContentType', None)
    if mime is None:
        _, ext = os.path.splitext(fname)
        mime = MIMES.get(ext, 'application/octet-stream')

    print('Uploading %s as https://s3.amazonaws.com/%s/%s [%s]' % (fname, obj.bucket_name, obj.key, acl))
    with io.open(fname, 'rb') as f:
        obj.put(
            Body=f,
            ContentType=mime,
            ACL=acl,
            **options
        )

def package_from_name(name):
    name = os.path.basename(name)
    package, _ = name.split('-', 1)
    package = re.sub(r'[-_.]+', '-', package)

    return package

def prepare(masks):
    for mask in masks:
        for fname in glob.glob(mask):
            if not os.path.isfile(fname):
                raise RuntimeError('Can not access file %s' % fname)

            name = os.path.basename(fname)
            _, ext = os.path.splitext(name)
            mime = MIMES.get(ext, 'application/octet-stream')

            yield SimpleNamespace(
                fname=fname,
                name=name,
                mime=mime
            )

def key_exists(s3, bucket, key):
    try:
        s3.Object(bucket, key).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        raise
    return True

def pip_conf():
    if sys.platform == 'linux':
        paths = [r'~/.config/pip/pip.conf', r'~/.pip/pip.conf', r'~/.piprc', r'/etc/pip.conf']
    elif sys.platform == 'win32':
        paths = [r'~/AppData/Roaming/pip/pip.ini', '~/pip/pip.ini']
    elif sys.platform == 'darwin':
        paths = [r'~/Library/Application Support/pip/pip.conf']
    else:
        assert False, sys.platform

    for fname in paths:
        fname = os.path.expanduser(fname)
        if os.path.isfile(fname):
            conf = configparser.ConfigParser()
            conf.read(fname)
            return conf

def find_from_pip_conf():
    conf = pip_conf()
    if conf is None:
        return None

    if 'ilabs.s3util' in conf and 'target' in conf['ilabs.s3util']:
        return conf['ilabs.s3util']['target']

    if 'global' not in conf or 'extra-index-url' not in conf['global']:
        return None

    extra_index_url = conf['global']['extra-index-url']

    # http://<bucket_name>.s3-website-<region>.amazonaws.com
    mtc = re.match(r'http://(.+)\.s3\-website\-(.+)\.amazonaws\.com(/.+)?$', extra_index_url)
    if mtc is None:
        return None

    bucket = mtc.group(1)
    assert '/' not in bucket
    prefix = mtc.group(3)
    if prefix:
        assert prefix.startswith('/')
        prefix = prefix.strip('/')
        if not prefix:
            prefix = None

    if prefix:
        return 's3://' + bucket + '/' + prefix
    else:
        return 's3://' + bucket

def parse_target(url):
    mtc = re.match(r's3://([^/]+)(/.+)?$', url)
    if mtc is None:
        raise RuntimeError('Invalid S3 url %r. Expect S3 url of the form: "s3://bucket/prefix" or "s3://bucket"' % url)

    bucket = mtc.group(1)
    prefix = mtc.group(2)
    if prefix is not None:
        assert prefix.startswith('/')
        prefix = prefix[1:]
        if not prefix:
            prefix = None
        elif prefix.endswith('/'):
            prefix = prefix[:-1]

    return bucket, prefix

def list_public_files(s3, bucket, prefix=None):
    if prefix is not None:
        prefix = prefix + '/'

    for key in s3.Bucket(bucket).objects.filter(Delimiter='/', Prefix=prefix):
        if not is_public_read(key):
            continue
        name = key.key
        if prefix is not None:
            name = name[len(prefix):]
            if name:
                yield name
        else:
            yield name

def is_public_read(key):
    for grant in key.Acl().grants:
        grantee_url = grant.get('Grantee', {}).get('URI')
        permission = grant.get('Permission')
        if grantee_url == 'http://acs.amazonaws.com/groups/global/AllUsers':
            if permission in ('READ', 'READ_ACP'):
                return True
    return False


TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Package Index</title>
</head>
<body>
{body}
</body>
</html>
'''

TEMPLATE_LINE = '''<a href="{name}">{name}</a><br>'''

MIMES = {
    '.gz' : 'application/gzip',
    '.xz' : 'application/x-xz',
    '.zip': 'application/zip',
    '.whl': 'application/zip',
}
