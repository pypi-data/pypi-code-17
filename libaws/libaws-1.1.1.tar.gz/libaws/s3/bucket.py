#coding:utf-8
import os
import argparse
from libaws.common.boto import * 
from libaws.common import config
from libaws.common.logger import logger

def put_bucket_policy(bucket,json_file):

    with open(json_file) as f:
        content = f.read()
        print content
        response = client_s3.put_bucket_policy(
            Bucket=bucket,Policy= content
        )

def handle_key_action(bucket,key,action):

    if action == "delete":
        delete_keys = []
        if key.endswith("/"):
            iter_keys = list_as_dir(bucket,key)
            for child_key in iter_keys:
                d = {
                    'Key':child_key
                }
                delete_keys.append(d)

            d = {
                'Key':key
            }
            delete_keys.append(d)

        delete_key_count = len(delete_keys)
        while True:
            max_del_number = 1000
            part_delete_keys = delete_keys[0:max_del_number]
            if 0 == len(part_delete_keys):
                break
            client_s3.delete_objects(Bucket=bucket,
                Delete={
                    'Objects':part_delete_keys
                }
            )
            delete_keys = delete_keys[max_del_number:]
        print 'delete total',delete_key_count-1,'child keys','in key',key
        print 'delete key',key,'success'

    elif action == "list":
        if key.endswith("/"):
            i = 0
            for child_key in list_as_dir(bucket,key):
                print child_key
                i += 1
            print 'total',i,'child keys in key',key

def list_as_dir(bucket,key):

    paginator = client_s3.get_paginator('list_objects')
    if key == "/":
        key = ""
    results = paginator.paginate(Bucket=bucket,Delimiter='/',Prefix=key)
    for prefix in results.search('CommonPrefixes'):
        if prefix is None:
            continue
        prefix = prefix.get('Prefix')
        for child_key in list_as_dir(bucket,prefix):
            yield child_key

    for res in results:
        if not res.has_key('Contents'):
            logger.error("key %s is not exist in bucket %s",key,bucket)
            continue
        contents = res['Contents']
        for content in contents:
            child_key = content['Key']
            if child_key == key:
                continue
            yield child_key

def main():
    parser = argparse.ArgumentParser()
    #指定下载的bucket,必须参数
    parser.add_argument("-name", "--name", type=str, dest="bucket",help='dest bucket to operate',required=True)
    parser.add_argument("-k", "--key", type=str, dest="key", help = 'bucket file to action')
    parser.add_argument("-a", "--action", type=str, dest="action", help = 'create delete key')
    #指定下载bucket中的文件,必须参数
    parser.add_argument("-put-bucket-policy", "--put-bucket-policy", action="store_true", dest="is_put_bucket_policy", help = 'set bucket policy',required=False)
    parser.add_argument("-json", "--json", type=str, dest="bucket_policy_json",help='bucket policy json file')

    args = parser.parse_args()
    bucket = args.bucket

    if args.is_put_bucket_policy:
        put_bucket_policy(bucket,args.bucket_policy_json)
   
    if args.action:
        handle_key_action(bucket,args.key,args.action)
