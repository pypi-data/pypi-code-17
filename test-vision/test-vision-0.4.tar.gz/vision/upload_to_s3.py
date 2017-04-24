#!/usr/bin/env python
"""
A Flask Application for searching through files in a directory.
 and uploading them to a customized s3 bucket
"""

import os
import json
import re
import sys
import logging

import requests
from flask import Flask
from gooey import Gooey, GooeyParser


app = Flask(__name__)


ALLOWED_FILE_EXTENSIONS = ['xml', 'csv']


def initialize_logger(output_dir):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(output_dir, "upload_error.log"), "w", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(output_dir, "upload.log"), "w")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


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


def check_if_bucket_in_s3(connection, bucket_name):
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


def get_s3_signed_url(filename, directory_path, muni):
    # Make post request with filename as postbody to
    # http://com-gwfathom-fsh-dev.us-west-2.elasticbeanstalk.com/Vision/HelloWorld and
    # get jobId and putUrl
    url = 'http://com-gwfathom-fsh-dev.us-west-2.elasticbeanstalk.com/Vision/Vision'
    payload = {'filename': filename, "muni": muni}
    headers = {'content-type': 'application/json'}
    get_jobid_and_puturl = requests.post(url, data=json.dumps(payload), headers=headers)
    response = get_jobid_and_puturl.json()
    put_url = response["putUrl"]
    job_id = response["jobId"]

    # Next, make a post request to putUrl
    # that is gotten from above with file path to be uploaded
    with open(os.path.join(directory_path, filename), 'r') as file_path_data:
        requests.put(put_url, data=file_path_data)
    # Make a get request to
    # http://com-gwfathom-fsh-dev.us-west-2.elasticbeanstalk.com/Vision/HelloWorld
    # with the jobId as args and get the status and reportUrl.
    get_job = requests.get('http://com-gwfathom-fsh-dev.us-west-2.elasticbeanstalk.com/Vision/Vision?jobId=' + job_id)
    get_res_json = get_job.json()
    report_url = get_res_json["reportUrl"]
    # Lastly, make a get request to the reportUrl and finish!
    post_report = requests.get(report_url)
    if post_report.status_code == 200:
        logging.info("Uploaded successfully!")
        return post_report.text
    else:
        logging.info("Not successful!")


def upload_s3(directory_path, directory_name, doc_type, muni):
    """
    Upload to s3
    """
    if check_if_directory(directory_path):
        for file in os.listdir(directory_path):
            if check_file_extension_type(file) == doc_type:
                try:
                    # Upload to S3
                    upload_detail = get_s3_signed_url(file, directory_path, muni)
                    logging.info(upload_detail)
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
    initialize_logger('')
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

    parser.add_argument('doc_type', choices=['xml', 'csv'], default='xml', nargs='?')

    args = parser.parse_args()

    doc_type = args.doc_type

    directory = args.directory
    muni = args.muni
    directory_path, directory_name = os.path.split(directory)
    logging.info("Directory %s found!" % directory_name)
    upload_s3(directory, directory_name, doc_type, muni)

if __name__ == '__main__':
    nonbuffered_stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    sys.stdout = nonbuffered_stdout
    main()
