from __future__ import print_function
import sys
from datetime import datetime

import plac
import boto3.session
import botocore.exceptions


# just to keep this code python 2.6 compatible
def total_seconds(timedelta):
    return (
        timedelta.microseconds + 0.0 +
        (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6


def error(*objs):
    print("ERROR", *objs, end='\n', file=sys.stderr)


@plac.annotations(
    profile_name=("""Name of AWSCLI profile to use for credentials""",
                  "option"),
    aws_access_key_id=("Your AWS Access Key ID", "option"),
    aws_secret_access_key=("Your AWS Secret Access Key", "option"),
    validate_bucket=("Make sure, the bucket really exists", "flag"),
    validate_key=("Make sure, the key really exists", "flag"),
    http=("Force the url to use http and not https", "flag"),
    expire_dt=("ISO formatted time of expiration, full seconds,"
               " 'Z' is obligatory, e.g. '2014-02-14T21:47:16Z'"),
    bucket_name="name of bucket", key_names="key names to generate tmpurl for")
def main(
        expire_dt,
        bucket_name,
        profile_name=None,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        validate_bucket=False,
        validate_key=False,
        http=False,
        *key_names):
    """Generate temporary url for accessing content of AWS S3 key.

    Temporary url includes expiration time, after which it rejects serving the
    content.

    Urls are printed one per line to stdout.

    For missing key names empty line is printed and error goes to stderr.

    If the bucket is versioned, tmp url will serve the latest version
    at the moment of request (version_id is not part of generated url).

    By default, bucket and key name existnence is not verified.

    Url is using https, unless `-http` is used.
    """
    session = boto3.session.Session(profile_name=profile_name,
                                    aws_access_key_id=aws_access_key_id,
                                    aws_secret_access_key=aws_secret_access_key)
    s3client = session.client("s3")
    s3 = session.resource("s3")
    expire_dt = datetime.strptime(expire_dt, "%Y-%m-%dT%H:%M:%SZ")

    params = {"Bucket": bucket_name}
    if http:
        params["HttpMethod"] = "http"

    if validate_bucket or validate_key:
        try:
            bucket = s3.Bucket(bucket_name)
            bucket.creation_date
        except botocore.exceptions.ClientError:
            error("Error: Bucket not found: ", bucket_name)
            return
    for key_name in key_names:
        if validate_key:
            try:
                key = s3.Object(bucket_name, key_name)
                key.get()
            except botocore.exceptions.NoSuchKey:
                error("Error: missing key: ", key_name)
                print("")
                continue
        # get a key object without version_id
        # (otherwise we get url to specific version)
        params["Key"] = key_name
        url = s3client.generate_presigned_url(
            "get_object",
            Params=params,
            ExpiresIn=total_seconds(expire_dt-datetime.utcnow()))
        print(url)


def placer():
    try:
        plac.call(main)
    except Exception as e:
        error(e)

if __name__ == "__main__":
    placer()
