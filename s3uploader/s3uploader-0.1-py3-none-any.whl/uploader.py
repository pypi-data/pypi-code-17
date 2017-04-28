import os

import boto3


class S3Uploader():
    def __init__(self, bucket_name):
        self.s3 = boto3.resource('s3')
        self.bucket_name = bucket_name
        self.count = 0

    def store_file(self, filename, store_paths=False, verbose=False):
        with open(filename, 'rb') as file:
            if store_paths:
                s3_object_name = filename
            else:
                s3_object_name = os.path.basename(filename)

            if verbose:
                print(' Uploading file ' + filename + ' to object ' + s3_object_name)

            try:
                obj = self.s3.Object(self.bucket_name, s3_object_name).put(Body=file)
            except Exception as e:
                print('!! Got an error while uploading file {file} to the S3 bucket {bucket}. Error: {error}'.format(
                    file=filename,
                    bucket=self.bucket_name,
                    error=e
                ))
            else:
                self.count += 1