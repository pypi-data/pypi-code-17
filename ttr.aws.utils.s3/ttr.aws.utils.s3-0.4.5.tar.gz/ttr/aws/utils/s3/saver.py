import time
import os.path
from .utils import gunzip_data


class ObjectVersionSaver(object):
    """
    """
    def __init__(self, s3, fname_factory, to_decompress):
        self.s3 = s3
        self.fname_factory = fname_factory
        self.to_decompress = to_decompress

    def save(self, bucket_name, key_name, version_id):
        """
        Raises:
            botocore.exceptions.ClientError: when missing credentials, missing
                bucket, missing object or object version or insufficient
                permissions.
        """
        key = self.s3.ObjectVersion(bucket_name, key_name, version_id).get()
        last_modified = key["LastModified"]
        fname = self.fname_factory(bucket_name,
                                   key_name,
                                   version_id,
                                   key)
        # TODO: modify for large files into streaming
        # gzip requires .tell and key["Body"] does not provide it
        with open(fname, "wb") as f:
            if key["ContentEncoding"] in self.to_decompress:
                f.write(gunzip_data(key["Body"].read()))
            else:
                f.write(key["Body"].read())
        # set modification time to the time, version was created in bucket
        tm = time.mktime(last_modified.timetuple())
        os.utime(fname, (tm, tm))
        return fname, key


class FnameFactory(object):

    def __init__(self):
        pass

    def last_modified(self, bucket_name, key_name, version_id, objdict):
        basename, ext = os.path.splitext(os.path.basename(key_name))
        templ = "{basename}.{LastModified:%Y-%m-%dT%H_%M_%SZ}{ext}"
        return templ.format(basename=basename,
                            ext=ext,
                            **objdict)

    def version_id(self, bucket_name, key_name, version_id, objdict):
        basename, ext = os.path.splitext(os.path.basename(key_name))
        templ = "{basename}.{version_id}{ext}"
        return templ.format(basename=basename,
                            ext=ext,
                            version_id=version_id,
                            **objdict)
