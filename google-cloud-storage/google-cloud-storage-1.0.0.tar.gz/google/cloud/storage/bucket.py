# Copyright 2014 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Create / interact with Google Cloud Storage buckets."""

import base64
import copy
import datetime
import json

import google.auth.credentials
import six

from google.cloud._helpers import _datetime_to_rfc3339
from google.cloud._helpers import _NOW
from google.cloud._helpers import _rfc3339_to_datetime
from google.cloud.exceptions import NotFound
from google.cloud.iterator import HTTPIterator
from google.cloud.storage._helpers import _PropertyMixin
from google.cloud.storage._helpers import _scalar_property
from google.cloud.storage._helpers import _validate_name
from google.cloud.storage.acl import BucketACL
from google.cloud.storage.acl import DefaultObjectACL
from google.cloud.storage.blob import Blob


def _blobs_page_start(iterator, page, response):
    """Grab prefixes after a :class:`~google.cloud.iterator.Page` started.

    :type iterator: :class:`~google.cloud.iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type page: :class:`~google.cloud.iterator.Page`
    :param page: The page that was just created.

    :type response: dict
    :param response: The JSON API response for a page of blobs.
    """
    page.prefixes = tuple(response.get('prefixes', ()))
    iterator.prefixes.update(page.prefixes)


def _item_to_blob(iterator, item):
    """Convert a JSON blob to the native object.

    .. note::

        This assumes that the ``bucket`` attribute has been
        added to the iterator after being created.

    :type iterator: :class:`~google.cloud.iterator.Iterator`
    :param iterator: The iterator that has retrieved the item.

    :type item: dict
    :param item: An item to be converted to a blob.

    :rtype: :class:`.Blob`
    :returns: The next blob in the page.
    """
    name = item.get('name')
    blob = Blob(name, bucket=iterator.bucket)
    blob._set_properties(item)
    return blob


class Bucket(_PropertyMixin):
    """A class representing a Bucket on Cloud Storage.

    :type client: :class:`google.cloud.storage.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the bucket (which requires a project).

    :type name: str
    :param name: The name of the bucket. Bucket names must start and end with a
                 number or letter.
    """

    _MAX_OBJECTS_FOR_ITERATION = 256
    """Maximum number of existing objects allowed in iteration.

    This is used in Bucket.delete() and Bucket.make_public().
    """

    _STORAGE_CLASSES = (
        'MULTI_REGIONAL',
        'REGIONAL',
        'NEARLINE',
        'COLDLINE',
        'STANDARD',  # alias for MULTI_REGIONAL/REGIONAL, based on location
        'DURABLE_REDUCED_AVAILABILITY',  # deprecated
    )
    """Allowed values for :attr:`storage_class`.

    See:
    https://cloud.google.com/storage/docs/json_api/v1/buckets#storageClass
    https://cloud.google.com/storage/docs/storage-classes
    """

    def __init__(self, client, name=None):
        name = _validate_name(name)
        super(Bucket, self).__init__(name=name)
        self._client = client
        self._acl = BucketACL(self)
        self._default_object_acl = DefaultObjectACL(self)

    def __repr__(self):
        return '<Bucket: %s>' % self.name

    @property
    def client(self):
        """The client bound to this bucket."""
        return self._client

    def blob(self, blob_name, chunk_size=None, encryption_key=None):
        """Factory constructor for blob object.

        .. note::
          This will not make an HTTP request; it simply instantiates
          a blob object owned by this bucket.

        :type blob_name: str
        :param blob_name: The name of the blob to be instantiated.

        :type chunk_size: int
        :param chunk_size: The size of a chunk of data whenever iterating
                           (1 MB). This must be a multiple of 256 KB per the
                           API specification.

        :type encryption_key: bytes
        :param encryption_key:
            Optional 32 byte encryption key for customer-supplied encryption.

        :rtype: :class:`google.cloud.storage.blob.Blob`
        :returns: The blob object created.
        """
        return Blob(name=blob_name, bucket=self, chunk_size=chunk_size,
                    encryption_key=encryption_key)

    def exists(self, client=None):
        """Determines whether or not this bucket exists.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :rtype: bool
        :returns: True if the bucket exists in Cloud Storage.
        """
        client = self._require_client(client)
        try:
            # We only need the status code (200 or not) so we seek to
            # minimize the returned payload.
            query_params = {'fields': 'name'}
            # We intentionally pass `_target_object=None` since fields=name
            # would limit the local properties.
            client._connection.api_request(
                method='GET', path=self.path,
                query_params=query_params, _target_object=None)
            # NOTE: This will not fail immediately in a batch. However, when
            #       Batch.finish() is called, the resulting `NotFound` will be
            #       raised.
            return True
        except NotFound:
            return False

    def create(self, client=None):
        """Creates current bucket.

        If the bucket already exists, will raise
        :class:`google.cloud.exceptions.Conflict`.

        This implements "storage.buckets.insert".

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.
        """
        client = self._require_client(client)
        query_params = {'project': client.project}
        properties = {key: self._properties[key] for key in self._changes}
        properties['name'] = self.name
        api_response = client._connection.api_request(
            method='POST', path='/b', query_params=query_params,
            data=properties, _target_object=self)
        self._set_properties(api_response)

    @property
    def acl(self):
        """Create our ACL on demand."""
        return self._acl

    @property
    def default_object_acl(self):
        """Create our defaultObjectACL on demand."""
        return self._default_object_acl

    @staticmethod
    def path_helper(bucket_name):
        """Relative URL path for a bucket.

        :type bucket_name: str
        :param bucket_name: The bucket name in the path.

        :rtype: str
        :returns: The relative URL path for ``bucket_name``.
        """
        return '/b/' + bucket_name

    @property
    def path(self):
        """The URL path to this bucket."""
        if not self.name:
            raise ValueError('Cannot determine path without bucket name.')

        return self.path_helper(self.name)

    def get_blob(self, blob_name, client=None):
        """Get a blob object by name.

        This will return None if the blob doesn't exist:

        .. literalinclude:: storage_snippets.py
          :start-after: [START get_blob]
          :end-before: [END get_blob]

        :type blob_name: str
        :param blob_name: The name of the blob to retrieve.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :rtype: :class:`google.cloud.storage.blob.Blob` or None
        :returns: The blob object if it exists, otherwise None.
        """
        client = self._require_client(client)
        blob = Blob(bucket=self, name=blob_name)
        try:
            response = client._connection.api_request(
                method='GET', path=blob.path, _target_object=blob)
            # NOTE: We assume response.get('name') matches `blob_name`.
            blob._set_properties(response)
            # NOTE: This will not fail immediately in a batch. However, when
            #       Batch.finish() is called, the resulting `NotFound` will be
            #       raised.
            return blob
        except NotFound:
            return None

    def list_blobs(self, max_results=None, page_token=None, prefix=None,
                   delimiter=None, versions=None,
                   projection='noAcl', fields=None, client=None):
        """Return an iterator used to find blobs in the bucket.

        :type max_results: int
        :param max_results: (Optional) Maximum number of blobs to return.

        :type page_token: str
        :param page_token: (Optional) Opaque marker for the next "page" of
                           blobs. If not passed, will return the first page
                           of blobs.

        :type prefix: str
        :param prefix: (Optional) prefix used to filter blobs.

        :type delimiter: str
        :param delimiter: (Optional) Delimiter, used with ``prefix`` to
                          emulate hierarchy.

        :type versions: bool
        :param versions: (Optional) Whether object versions should be returned
                         as separate blobs.

        :type projection: str
        :param projection: (Optional) If used, must be 'full' or 'noAcl'.
                           Defaults to ``'noAcl'``. Specifies the set of
                           properties to return.

        :type fields: str
        :param fields: (Optional) Selector specifying which fields to include
                       in a partial response. Must be a list of fields. For
                       example to get a partial response with just the next
                       page token and the language of each blob returned:
                       ``'items/contentLanguage,nextPageToken'``.

        :type client: :class:`~google.cloud.storage.client.Client`
        :param client: (Optional) The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :rtype: :class:`~google.cloud.iterator.Iterator`
        :returns: Iterator of all :class:`~google.cloud.storage.blob.Blob`
                  in this bucket matching the arguments.
        """
        extra_params = {}

        if prefix is not None:
            extra_params['prefix'] = prefix

        if delimiter is not None:
            extra_params['delimiter'] = delimiter

        if versions is not None:
            extra_params['versions'] = versions

        extra_params['projection'] = projection

        if fields is not None:
            extra_params['fields'] = fields

        client = self._require_client(client)
        path = self.path + '/o'
        iterator = HTTPIterator(
            client=client, path=path, item_to_value=_item_to_blob,
            page_token=page_token, max_results=max_results,
            extra_params=extra_params, page_start=_blobs_page_start)
        iterator.bucket = self
        iterator.prefixes = set()
        return iterator

    def delete(self, force=False, client=None):
        """Delete this bucket.

        The bucket **must** be empty in order to submit a delete request. If
        ``force=True`` is passed, this will first attempt to delete all the
        objects / blobs in the bucket (i.e. try to empty the bucket).

        If the bucket doesn't exist, this will raise
        :class:`google.cloud.exceptions.NotFound`.  If the bucket is not empty
        (and ``force=False``), will raise
        :class:`google.cloud.exceptions.Conflict`.

        If ``force=True`` and the bucket contains more than 256 objects / blobs
        this will cowardly refuse to delete the objects (or the bucket). This
        is to prevent accidental bucket deletion and to prevent extremely long
        runtime of this method.

        :type force: bool
        :param force: If True, empties the bucket's objects then deletes it.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :raises: :class:`ValueError` if ``force`` is ``True`` and the bucket
                 contains more than 256 objects / blobs.
        """
        client = self._require_client(client)
        if force:
            blobs = list(self.list_blobs(
                max_results=self._MAX_OBJECTS_FOR_ITERATION + 1,
                client=client))
            if len(blobs) > self._MAX_OBJECTS_FOR_ITERATION:
                message = (
                    'Refusing to delete bucket with more than '
                    '%d objects. If you actually want to delete '
                    'this bucket, please delete the objects '
                    'yourself before calling Bucket.delete().'
                ) % (self._MAX_OBJECTS_FOR_ITERATION,)
                raise ValueError(message)

            # Ignore 404 errors on delete.
            self.delete_blobs(blobs, on_error=lambda blob: None,
                              client=client)

        # We intentionally pass `_target_object=None` since a DELETE
        # request has no response value (whether in a standard request or
        # in a batch request).
        client._connection.api_request(
            method='DELETE', path=self.path, _target_object=None)

    def delete_blob(self, blob_name, client=None):
        """Deletes a blob from the current bucket.

        If the blob isn't found (backend 404), raises a
        :class:`google.cloud.exceptions.NotFound`.

        For example:

        .. literalinclude:: storage_snippets.py
          :start-after: [START delete_blob]
          :end-before: [END delete_blob]

        :type blob_name: str
        :param blob_name: A blob name to delete.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :raises: :class:`google.cloud.exceptions.NotFound` (to suppress
                 the exception, call ``delete_blobs``, passing a no-op
                 ``on_error`` callback, e.g.:

        .. literalinclude:: storage_snippets.py
            :start-after: [START delete_blobs]
            :end-before: [END delete_blobs]

        """
        client = self._require_client(client)
        blob_path = Blob.path_helper(self.path, blob_name)
        # We intentionally pass `_target_object=None` since a DELETE
        # request has no response value (whether in a standard request or
        # in a batch request).
        client._connection.api_request(
            method='DELETE', path=blob_path, _target_object=None)

    def delete_blobs(self, blobs, on_error=None, client=None):
        """Deletes a list of blobs from the current bucket.

        Uses :meth:`delete_blob` to delete each individual blob.

        :type blobs: list
        :param blobs: A list of :class:`~google.cloud.storage.blob.Blob`-s or
                      blob names to delete.

        :type on_error: callable
        :param on_error: (Optional) Takes single argument: ``blob``. Called
                         called once for each blob raising
                         :class:`~google.cloud.exceptions.NotFound`;
                         otherwise, the exception is propagated.

        :type client: :class:`~google.cloud.storage.client.Client`
        :param client: (Optional) The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :raises: :class:`~google.cloud.exceptions.NotFound` (if
                 `on_error` is not passed).
        """
        for blob in blobs:
            try:
                blob_name = blob
                if not isinstance(blob_name, six.string_types):
                    blob_name = blob.name
                self.delete_blob(blob_name, client=client)
            except NotFound:
                if on_error is not None:
                    on_error(blob)
                else:
                    raise

    def copy_blob(self, blob, destination_bucket, new_name=None,
                  client=None, preserve_acl=True):
        """Copy the given blob to the given bucket, optionally with a new name.

        :type blob: :class:`google.cloud.storage.blob.Blob`
        :param blob: The blob to be copied.

        :type destination_bucket: :class:`google.cloud.storage.bucket.Bucket`
        :param destination_bucket: The bucket into which the blob should be
                                   copied.

        :type new_name: str
        :param new_name: (optional) the new name for the copied file.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :type preserve_acl: bool
        :param preserve_acl: Optional. Copies ACL from old blob to new blob.
                             Default: True.

        :rtype: :class:`google.cloud.storage.blob.Blob`
        :returns: The new Blob.
        """
        client = self._require_client(client)
        if new_name is None:
            new_name = blob.name
        new_blob = Blob(bucket=destination_bucket, name=new_name)
        api_path = blob.path + '/copyTo' + new_blob.path
        copy_result = client._connection.api_request(
            method='POST', path=api_path, _target_object=new_blob)
        if not preserve_acl:
            new_blob.acl.save(acl={}, client=client)
        new_blob._set_properties(copy_result)
        return new_blob

    def rename_blob(self, blob, new_name, client=None):
        """Rename the given blob using copy and delete operations.

        Effectively, copies blob to the same bucket with a new name, then
        deletes the blob.

        .. warning::

          This method will first duplicate the data and then delete the
          old blob.  This means that with very large objects renaming
          could be a very (temporarily) costly or a very slow operation.

        :type blob: :class:`google.cloud.storage.blob.Blob`
        :param blob: The blob to be renamed.

        :type new_name: str
        :param new_name: The new name for this blob.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :rtype: :class:`Blob`
        :returns: The newly-renamed blob.
        """
        new_blob = self.copy_blob(blob, self, new_name, client=client)
        blob.delete(client=client)
        return new_blob

    @property
    def cors(self):
        """Retrieve or set CORS policies configured for this bucket.

        See: http://www.w3.org/TR/cors/ and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :setter: Set CORS policies for this bucket.
        :getter: Gets the CORS policies for this bucket.

        :rtype: list of dictionaries
        :returns: A sequence of mappings describing each CORS policy.
        """
        return [copy.deepcopy(policy)
                for policy in self._properties.get('cors', ())]

    @cors.setter
    def cors(self, entries):
        """Set CORS policies configured for this bucket.

        See: http://www.w3.org/TR/cors/ and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :type entries: list of dictionaries
        :param entries: A sequence of mappings describing each CORS policy.
        """
        self._patch_property('cors', entries)

    @property
    def etag(self):
        """Retrieve the ETag for the bucket.

        See: https://tools.ietf.org/html/rfc2616#section-3.11 and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: str or ``NoneType``
        :returns: The bucket etag or ``None`` if the property is not
                  set locally.
        """
        return self._properties.get('etag')

    @property
    def id(self):
        """Retrieve the ID for the bucket.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: str or ``NoneType``
        :returns: The ID of the bucket or ``None`` if the property is not
                  set locally.
        """
        return self._properties.get('id')

    @property
    def lifecycle_rules(self):
        """Lifecycle rules configured for this bucket.

        See: https://cloud.google.com/storage/docs/lifecycle and
             https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: list(dict)
        :returns: A sequence of mappings describing each lifecycle rule.
        """
        info = self._properties.get('lifecycle', {})
        return [copy.deepcopy(rule) for rule in info.get('rule', ())]

    @lifecycle_rules.setter
    def lifecycle_rules(self, rules):
        self._patch_property('lifecycle', {'rule': rules})

    location = _scalar_property('location')
    """Retrieve location configured for this bucket.

    See: https://cloud.google.com/storage/docs/json_api/v1/buckets and
    https://cloud.google.com/storage/docs/bucket-locations

    If the property is not set locally, returns ``None``.

    :rtype: str or ``NoneType``
    """

    def get_logging(self):
        """Return info about access logging for this bucket.

        See: https://cloud.google.com/storage/docs/access-logs#status

        :rtype: dict or None
        :returns: a dict w/ keys, ``logBucket`` and ``logObjectPrefix``
                  (if logging is enabled), or None (if not).
        """
        info = self._properties.get('logging')
        return copy.deepcopy(info)

    def enable_logging(self, bucket_name, object_prefix=''):
        """Enable access logging for this bucket.

        See: https://cloud.google.com/storage/docs/access-logs

        :type bucket_name: str
        :param bucket_name: name of bucket in which to store access logs

        :type object_prefix: str
        :param object_prefix: prefix for access log filenames
        """
        info = {'logBucket': bucket_name, 'logObjectPrefix': object_prefix}
        self._patch_property('logging', info)

    def disable_logging(self):
        """Disable access logging for this bucket.

        See: https://cloud.google.com/storage/docs/access-logs#disabling
        """
        self._patch_property('logging', None)

    @property
    def metageneration(self):
        """Retrieve the metageneration for the bucket.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: int or ``NoneType``
        :returns: The metageneration of the bucket or ``None`` if the property
                  is not set locally.
        """
        metageneration = self._properties.get('metageneration')
        if metageneration is not None:
            return int(metageneration)

    @property
    def owner(self):
        """Retrieve info about the owner of the bucket.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: dict or ``NoneType``
        :returns: Mapping of owner's role/ID. If the property is not set
                  locally, returns ``None``.
        """
        return copy.deepcopy(self._properties.get('owner'))

    @property
    def project_number(self):
        """Retrieve the number of the project to which the bucket is assigned.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: int or ``NoneType``
        :returns: The project number that owns the bucket or ``None`` if the
                  property is not set locally.
        """
        project_number = self._properties.get('projectNumber')
        if project_number is not None:
            return int(project_number)

    @property
    def self_link(self):
        """Retrieve the URI for the bucket.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: str or ``NoneType``
        :returns: The self link for the bucket or ``None`` if the property is
                  not set locally.
        """
        return self._properties.get('selfLink')

    @property
    def storage_class(self):
        """Retrieve the storage class for the bucket.

        See: https://cloud.google.com/storage/docs/storage-classes

        :rtype: str or ``NoneType``
        :returns: If set, one of "MULTI_REGIONAL", "REGIONAL",
                  "NEARLINE", "COLDLINE", "STANDARD", or
                  "DURABLE_REDUCED_AVAILABILITY", else ``None``.
        """
        return self._properties.get('storageClass')

    @storage_class.setter
    def storage_class(self, value):
        """Set the storage class for the bucket.

        See: https://cloud.google.com/storage/docs/storage-classes

        :type value: str
        :param value: one of "MULTI_REGIONAL", "REGIONAL", "NEARLINE",
                      "COLDLINE", "STANDARD", or "DURABLE_REDUCED_AVAILABILITY"
        """
        if value not in self._STORAGE_CLASSES:
            raise ValueError('Invalid storage class: %s' % (value,))
        self._patch_property('storageClass', value)

    @property
    def time_created(self):
        """Retrieve the timestamp at which the bucket was created.

        See: https://cloud.google.com/storage/docs/json_api/v1/buckets

        :rtype: :class:`datetime.datetime` or ``NoneType``
        :returns: Datetime object parsed from RFC3339 valid timestamp, or
                  ``None`` if the property is not set locally.
        """
        value = self._properties.get('timeCreated')
        if value is not None:
            return _rfc3339_to_datetime(value)

    @property
    def versioning_enabled(self):
        """Is versioning enabled for this bucket?

        See:  https://cloud.google.com/storage/docs/object-versioning for
        details.

        :rtype: bool
        :returns: True if enabled, else False.
        """
        versioning = self._properties.get('versioning', {})
        return versioning.get('enabled', False)

    @versioning_enabled.setter
    def versioning_enabled(self, value):
        """Enable versioning for this bucket.

        See:  https://cloud.google.com/storage/docs/object-versioning for
        details.

        :type value: convertible to boolean
        :param value: should versioning be anabled for the bucket?
        """
        self._patch_property('versioning', {'enabled': bool(value)})

    def configure_website(self, main_page_suffix=None, not_found_page=None):
        """Configure website-related properties.

        See: https://cloud.google.com/storage/docs/hosting-static-website

        .. note::
          This (apparently) only works
          if your bucket name is a domain name
          (and to do that, you need to get approved somehow...).

        If you want this bucket to host a website, just provide the name
        of an index page and a page to use when a blob isn't found:

        .. literalinclude:: storage_snippets.py
          :start-after: [START configure_website]
          :end-before: [END configure_website]

        You probably should also make the whole bucket public:

        .. literalinclude:: storage_snippets.py
            :start-after: [START make_public]
            :end-before: [END make_public]

        This says: "Make the bucket public, and all the stuff already in
        the bucket, and anything else I add to the bucket.  Just make it
        all public."

        :type main_page_suffix: str
        :param main_page_suffix: The page to use as the main page
                                 of a directory.
                                 Typically something like index.html.

        :type not_found_page: str
        :param not_found_page: The file to use when a page isn't found.
        """
        data = {
            'mainPageSuffix': main_page_suffix,
            'notFoundPage': not_found_page,
        }
        self._patch_property('website', data)

    def disable_website(self):
        """Disable the website configuration for this bucket.

        This is really just a shortcut for setting the website-related
        attributes to ``None``.
        """
        return self.configure_website(None, None)

    def make_public(self, recursive=False, future=False, client=None):
        """Make a bucket public.

        If ``recursive=True`` and the bucket contains more than 256
        objects / blobs this will cowardly refuse to make the objects public.
        This is to prevent extremely long runtime of this method.

        :type recursive: bool
        :param recursive: If True, this will make all blobs inside the bucket
                          public as well.

        :type future: bool
        :param future: If True, this will make all objects created in the
                       future public as well.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.
        """
        self.acl.all().grant_read()
        self.acl.save(client=client)

        if future:
            doa = self.default_object_acl
            if not doa.loaded:
                doa.reload(client=client)
            doa.all().grant_read()
            doa.save(client=client)

        if recursive:
            blobs = list(self.list_blobs(
                projection='full',
                max_results=self._MAX_OBJECTS_FOR_ITERATION + 1,
                client=client))
            if len(blobs) > self._MAX_OBJECTS_FOR_ITERATION:
                message = (
                    'Refusing to make public recursively with more than '
                    '%d objects. If you actually want to make every object '
                    'in this bucket public, please do it on the objects '
                    'yourself.'
                ) % (self._MAX_OBJECTS_FOR_ITERATION,)
                raise ValueError(message)

            for blob in blobs:
                blob.acl.all().grant_read()
                blob.acl.save(client=client)

    def generate_upload_policy(
            self, conditions, expiration=None, client=None):
        """Create a signed upload policy for uploading objects.

        This method generates and signs a policy document. You can use
        `policy documents`_ to allow visitors to a website to upload files to
        Google Cloud Storage without giving them direct write access.

        For example:

        .. literalinclude:: storage_snippets.py
            :start-after: [START policy_document]
            :end-before: [END policy_document]

        .. _policy documents:
            https://cloud.google.com/storage/docs/xml-api\
            /post-object#policydocument

        :type expiration: datetime
        :param expiration: Optional expiration in UTC. If not specified, the
                           policy will expire in 1 hour.

        :type conditions: list
        :param conditions: A list of conditions as described in the
                          `policy documents`_ documentation.

        :type client: :class:`~google.cloud.storage.client.Client`
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.

        :rtype: dict
        :returns: A dictionary of (form field name, form field value) of form
                  fields that should be added to your HTML upload form in order
                  to attach the signature.
        """
        client = self._require_client(client)
        credentials = client._base_connection.credentials

        if not isinstance(credentials, google.auth.credentials.Signing):
            auth_uri = ('http://google-cloud-python.readthedocs.io/en/latest/'
                        'google-cloud-auth.html#setting-up-a-service-account')
            raise AttributeError(
                'you need a private key to sign credentials.'
                'the credentials you are currently using %s '
                'just contains a token. see %s for more '
                'details.' % (type(credentials), auth_uri))

        if expiration is None:
            expiration = _NOW() + datetime.timedelta(hours=1)

        conditions = conditions + [
            {'bucket': self.name},
        ]

        policy_document = {
            'expiration': _datetime_to_rfc3339(expiration),
            'conditions': conditions,
        }

        encoded_policy_document = base64.b64encode(
            json.dumps(policy_document).encode('utf-8'))
        signature = base64.b64encode(
            credentials.sign_bytes(encoded_policy_document))

        fields = {
            'bucket': self.name,
            'GoogleAccessId': credentials.signer_email,
            'policy': encoded_policy_document.decode('utf-8'),
            'signature': signature.decode('utf-8'),
        }

        return fields
