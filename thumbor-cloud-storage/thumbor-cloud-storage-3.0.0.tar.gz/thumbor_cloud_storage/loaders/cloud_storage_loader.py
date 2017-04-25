from tornado.concurrent import return_future
from gcloud import storage
from collections import defaultdict

buckets = defaultdict(dict)

@return_future
def load(context, path, callback):
    bucket_id  = context.config.get("CLOUD_STORAGE_BUCKET_ID")
    project_id = context.config.get("CLOUD_STORAGE_PROJECT_ID")
    bucket = buckets[project_id].get(bucket_id, None)
    if bucket is None:
        client = storage.Client(project_id)
        bucket = client.get_bucket(bucket_id)
        buckets[project_id][bucket_id] = bucket

    blob = bucket.get_blob(path)
    if blob:
        callback(blob.download_as_string())
    else:
        callback(blob)
