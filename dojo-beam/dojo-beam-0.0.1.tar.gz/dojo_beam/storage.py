from __future__ import absolute_import, print_function, unicode_literals

import apache_beam as beam

from googleapiclient import discovery
from apache_beam.io import ReadFromText, WriteToText, WriteToTFRecord

from dojo.storage import Storage
from dojo.vanilla.stores.google_storage import google_cloud_credentials

from .transform import ConvertFrom, ConvertTo


class BeamStorage(Storage):

    def read(self, path):
        p = self.dataset.pipeline
        input_uri = self.as_uri(path)
        rows = (p | 'read ' + input_uri >> ReadFromText(str(input_uri)))
        return rows

    def write(self, path, rows, format='json'):
        extensions = {
            'json': '.json',
            'csv': '.csv',
            'tf': '.tfrecord.gz'
        }
        writers = {
            'json': WriteToText,
            'csv': WriteToText,
            'tf': WriteToTFRecord
        }
        extension = extensions.get(format)
        writer = writers[format]
        output_uri = self.as_uri(path)
        rows = rows | 'convert ' + output_uri + ' ' + format >> beam.ParDo(ConvertTo(format))
        rows | 'write ' + output_uri + ' ' + format >> writer(str(output_uri), file_name_suffix=extension)
        return rows

    def list_keys(self, prefix):
        raise NotImplementedError()


class BeamLocalFileStore(BeamStorage):

    def as_uri(self, path):
        return '%s://%s' % (self.config['protocol'], path)


class BeamGoogleStorageStore(BeamStorage):

    def setup(self):
        credentials = google_cloud_credentials(self.secrets['connection'])
        self.service = discovery.build('storage', 'v1', credentials=credentials)

    def read(self, path):
        return super(BeamGoogleStorageStore, self).read(str(path))

    def write(self, path, rows, format='json'):
        return super(BeamGoogleStorageStore, self).write(str(path), rows, format=format)

    def list_keys(self, prefix):
        req = self.service.objects().list(bucket=self.config['bucket'], prefix=prefix, delimiter='/')
        keys = []
        while req:
            resp = req.execute()
            keys += resp.get('prefixes', [])
            keys += [key['name'] for key in resp.get('items', [])]
            req = self.service.objects().list_next(req, resp)
        return keys

    def as_uri(self, path):
        return '%s://%s/%s' % (self.config['protocol'], self.config['bucket'], path)


class BeamS3Store(BeamStorage):
    pass
