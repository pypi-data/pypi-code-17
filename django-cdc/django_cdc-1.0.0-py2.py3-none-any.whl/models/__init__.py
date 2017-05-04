import boto3

from django_cdc import settings

# initialize lambda function
lambda_client = None

try:
    lambda_client = boto3.client(
        "lambda", region_name=settings.AWS_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
except:
    pass
