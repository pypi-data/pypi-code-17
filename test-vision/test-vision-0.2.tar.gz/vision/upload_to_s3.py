#!/usr/bin/env python
"""
A Flask Application for searching through files in a directory.
 and uploading them to a customized s3 bucket
"""

import os
import json
import re
import sys

from boto.s3.connection import S3Connection
from boto.s3.key import Key as S3Key
from flask import Flask
from gooey import Gooey, GooeyParser
from vision.utils.loggerinitializer import *


initialize_logger('')

app = Flask(__name__)


ALLOWED_FILE_EXTENSIONS = ['xml', 'csv']

# connection = S3Connection(app.config['AWS_ACCESS_KEY_ID'], app.config[
#     'AWS_SECRET_ACCESS_KEY'])

connection = S3Connection(
    'AKIAITZPF2TWTUUWWNXA', 'VGCtFOdo3HgCBw8fTm294Up8/0LYJmlSm5Z6XCO4')


def check_file_extension_type(filename):
    """
    Check for accepted File Extension Types
    """
    file_extension = os.path.splitext(filename)[1][1:].lower()
    if file_extension:
        for ext in ALLOWED_FILE_EXTENSIONS:
            if file_extension in ext:
                return file_extension


def get_selected_file_name_without_date(filename):
    """
    Extract file name without the date prefixed or suffixed to it
    """
    file_name = filename.split('.')[0]
    date_in_filename = re.search(r'[0-9]{2,4}[\/,:\-][0-9]{2}[\/,:\-][0-9]{2,4}', file_name)
    try:
        only_date = date_in_filename.group()
        only_file_name = file_name.strip(only_date)
        return only_file_name
    except Exception:
        logging.info("No date in %s" % filename)
        return filename


def check_if_directory(directory):
    """
    Check if directory exists
    """
    if not os.path.isdir(directory):
        raise IOError("Not a directory")
    return directory


def check_if_bucket_in_s3(bucket_name):
    """
    Finds existing bucket using the directory name
    in s3 or creates a new one if none exists
    """
    if connection.lookup(bucket_name) is None:
        logging.info("Creating a new S3 Bucket")
        bucket = connection.create_bucket(bucket_name)
        logging.info("S3 bucket %s created" % bucket_name)
    else:
        logging.info("Found bucket %s" % bucket_name)
        bucket = bucket_name
    return bucket


def upload_s3(directory_path, directory_name, doc_type):
    """
    Upload to s3
    """
    bucket_name = check_if_bucket_in_s3(directory_name)
    bucket = connection.get_bucket(bucket_name)
    obj = S3Key(bucket)

    if check_if_directory(directory_path):
        for file in os.listdir(directory_path):
            if check_file_extension_type(file) == doc_type:
                try:
                    # Read the content of the file
                    with open(os.path.join(directory_path, file), 'r') as data_file:
                        file_contents = data_file.read().replace('\n', '')
                    obj.name = get_selected_file_name_without_date(file)
                    logging.info("Uploading %s to %s S3 bucket" % (obj.name, bucket_name))
                    obj.set_contents_from_string(file_contents)
                    obj.set_acl('public-read')
                    logging.info("%s uploaded successfully to %s bucket" % (obj.name, bucket_name))
                # error handling
                except Exception as error:
                    logging.error("File not uploaded to S3 error - $s" % error)
            else:
                continue


@Gooey
def main():
    """
    Main function that gets args from the gooey GUI
    """
    parser = GooeyParser(description='Upload files to s3')
    stored_args = {}
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    args_file = "{}-args.json".format(script_name)
    if os.path.isfile(args_file):
        with open(args_file) as data_file:
            stored_args = json.load(data_file)

    parser.add_argument(
        'directory',
        action='store',
        default=stored_args.get('directory'),
        help='Directory that contains XML files')
    parser.add_argument(
        'muni',
        action='store',
        default=stored_args.get('muni'),
        help='The muni to which the document applies, from the configuration')
    parser.add_argument(
        'system_meter',
        action='store',
        default=stored_args.get('system_meter'),
        help='The meterSystem, if any, to which the document applies')
    parser.add_argument(
        'username',
        action='store',
        default=stored_args.get('username'),
        help='Username configured for this Vision instance')
    parser.add_argument(
        'password',
        action='store',
        default=stored_args.get('password'),
        help='Password configured for this Vision instance')
    parser.add_argument('doc_type', choices=['xml', 'csv'], default='xml', nargs='?')

    args = parser.parse_args()

    doc_type = args.doc_type

    directory = args.directory
    directory_path, directory_name = os.path.split(directory)
    logging.info("Directory %s found!" % directory_name)
    upload_s3(directory, directory_name, doc_type)

if __name__ == '__main__':
    nonbuffered_stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    sys.stdout = nonbuffered_stdout
    main()
