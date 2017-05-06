import os

config = {
    'appid': int(os.getenv('QCOS_APPID', 0)),
    'secret_id': os.getenv('QCOS_SECRET_ID', '').decode('utf-8'),
    'secret_key': os.getenv('QCOS_SECRET_KEY', '').decode('utf-8'),
    'region': os.getenv('QCOS_REGION', '').decode('utf-8'),
    'bucket_name': os.getenv('QCOS_BUCKET_NAME', '').decode('utf-8')
}
