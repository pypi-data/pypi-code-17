#!/usr/bin/env python
# Upload a file to an Amazon S3 bucket
import argparse

from s3uploader.uploader import S3Uploader

parser = argparse.ArgumentParser(description='Upload files to an Amazon S3 bucket. version 0.1')
parser.add_argument('--verbose', action='store_true', help='Give verbose output while uploading files')
parser.add_argument('--store-paths', action='store_true', help='Store the file path in the S3 object name')
parser.add_argument('bucket', help='Name of the S3 bucket to use')
parser.add_argument('file', nargs='+', help='File to upload to the S3 bucket')


def run():
    args = parser.parse_args()

    uploader = S3Uploader(args.bucket)
    verbose = args.verbose
    store_paths = args.store_paths

    if verbose:
        print('Starting upload for {count} files to S3 bucket {bucket}:'.format(
            count=len(args.file),
            bucket=uploader.bucket_name
        ))

    for filename in args.file:
        uploader.store_file(filename, store_paths=store_paths, verbose=verbose)

    if verbose:
        print('Uploaded {count} files to the S3 bucket {bucket}'.format(
            count=uploader.count,
            bucket=uploader.bucket_name
        ))
