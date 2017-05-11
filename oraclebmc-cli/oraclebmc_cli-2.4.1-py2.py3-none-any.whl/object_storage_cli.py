# coding: utf-8
# Copyright (c) 2016, 2017, Oracle and/or its affiliates. All rights reserved.

import click
import os
import os.path
import sys
from .packages.oraclebmc import exceptions
from .packages.oraclebmc.object_storage import models
from .cli_root import cli
from .cli_util import render, render_response, parse_json_parameter, help_option, help_option_group, build_client, confirm_delete_option, wrap_exceptions, filter_object_headers
from .packages.oraclebmc.object_storage import UploadManager


OBJECT_LIST_PAGE_SIZE = 100

MEBIBYTE = 1024 * 1024

OBJECT_GET_CHUNK_SIZE = MEBIBYTE

OBJECT_PUT_DISPLAY_HEADERS = {
    "etag",
    "opc-content-md5",
    "last-modified",
    "opc-multipart-md5"
}


@click.group(name='os', help="""Object Storage Service""")
@help_option_group
def objectstorage():
    pass


cli.add_command(objectstorage)


@click.group(name='ns')
@help_option_group
def ns():
    pass


@click.command(name='get')
@help_option
@click.pass_context
@wrap_exceptions
def ns_get(ctx):
    """
    Gets the name of the namespace for the user making the request.

    Example:
        bmcs os ns get
    """
    client = build_client('os', ctx)
    render_response(client.get_namespace(opc_client_request_id=ctx.obj['request_id']))


objectstorage.add_command(ns)
ns.add_command(ns_get)


@click.group('bucket')
@help_option_group
def bucket():
    pass


@click.command(name='list')
@click.option('-ns', '--namespace', required=True, help='The top-level namespace used for the request.')
@click.option('--compartment-id', required=True, help='The compartment ID to return buckets for.')
@click.option('--limit', default=100, show_default=True, help='The maximum number of items to return.')
@help_option
@click.pass_context
@wrap_exceptions
def bucket_list(ctx, namespace, compartment_id, limit):
    """
    Lists the `BucketSummary`s in a namespace. A `BucketSummary` contains only summary fields for the bucket
    and not fields such as the user-defined metadata.

    Example:
        bmcs os bucket list -ns mynamespace --compartment-id ocid1.compartment.oc1..aaaaaaaarhifmvrvuqtye5q65flzp3pp2jojdc6rck6copzqck3ukcypxfga
    """

    client = build_client('os', ctx)

    args = {
        'opc_client_request_id': ctx.obj['request_id']
    }

    all_buckets = []

    while limit > 0:
        response = client.list_buckets(
            namespace,
            compartment_id,
            **args
        )
        buckets = response.data[:limit]
        next_page = response.headers.get('opc-next-page', None)

        all_buckets.extend(buckets)

        if next_page:
            limit -= len(buckets)
            args['page'] = next_page
        else:
            limit = 0

    render(all_buckets, response.headers)


@click.command(name='create')
@click.option('-ns', '--namespace', required=True, help='The top-level namespace used for the request.')
@click.option('--compartment-id', required=True, help='The ID of the compartment in which to create the bucket.')
@click.option('--name', required=True, help='The name of the bucket.')
@click.option('--metadata', help='Arbitrary string keys and values for user-defined metadata. Must be in JSON format. Example: \'{"key1":"value1","key2":"value2"}\'')
@help_option
@click.pass_context
@wrap_exceptions
def bucket_create(ctx, namespace, name, compartment_id, metadata):
    """
    Creates a bucket in the given namespace with a bucket name and optional user-defined metadata.

    Example:
        bmcs os bucket create -ns mynamespace --name mybucket --compartment-id ocid1.compartment.oc1..aaaaaaaarhifmvrvuqtye5q65flzp3pp2jojdc6rck6copzqck3ukcypxfga --metadata '{"key1":"value1","key2":"value2"}'
    """

    bucket_details = models.CreateBucketDetails()
    bucket_details.compartment_id = compartment_id
    bucket_details.name = name
    bucket_details.metadata = parse_json_parameter("metadata", metadata, default={})
    client = build_client('os', ctx)
    render_response(client.create_bucket(namespace, bucket_details, opc_client_request_id=ctx.obj['request_id']))


@click.command(name='update')
@click.option('-ns', '--namespace', required=True, help='The top-level namespace used for the request.')
@click.option('--name', required=True, help='The name of the bucket.')
@click.option('--if-match', help='The entity tag to match.')
@click.option('--metadata', help='Arbitrary string keys and values for user-defined metadata. Must be in JSON format. Values will be appended to existing metadata. To remove a key, set it to null. Example: \'{"key1":"value1","key2":null}\'')
@help_option
@click.pass_context
@wrap_exceptions
def bucket_update(ctx, namespace, name, if_match, metadata):
    """
    Updates a bucket's user-defined metadata.

    Example:
        bmcs os bucket update -ns mynamespace --name mybucket --metadata '{"key1":"value1","key2":"value2"}'
    """

    bucket_details = models.UpdateBucketDetails()
    bucket_details.name = name
    bucket_details.metadata = parse_json_parameter("metadata", metadata, default={})

    client = build_client('os', ctx)
    render_response(client.update_bucket(
        namespace,
        name,
        bucket_details,
        if_match=if_match,
        opc_client_request_id=ctx.obj['request_id']
    ))


@click.command(name='get')
@click.option('-ns', '--namespace', required=True, help='The top-level namespace used for the request.')
@click.option('--name', required=True, help='The name of the bucket.')
@click.option('--if-match', help='The entity tag to match.')
@click.option('--if-none-match', help='The entity tag to avoid matching.')
@help_option
@click.pass_context
@wrap_exceptions
def bucket_get(ctx, namespace, name, if_match, if_none_match):
    """
    Gets the current representation of the given bucket in the given namespace.

    Example:
        bmcs os bucket get -ns mynamespace --name mybucket
    """
    client = build_client('os', ctx)
    render_response(client.get_bucket(
        namespace,
        name,
        if_match=if_match,
        if_none_match=if_none_match,
        opc_client_request_id=ctx.obj['request_id']
    ))


@click.command(name='delete')
@click.option('-ns', '--namespace', required=True, help='The top-level namespace used for the request.')
@click.option('--name', required=True, help='The name of the bucket.')
@click.option('--if-match', help='The entity tag to match.')
@confirm_delete_option
@help_option
@click.pass_context
@wrap_exceptions
def bucket_delete(ctx, namespace, name, if_match):
    """
    Deletes a bucket if it is already empty.

    Example:
        bmcs os bucket delete -ns mynamespace --name mybucket
    """
    client = build_client('os', ctx)
    render_response(client.delete_bucket(namespace, name, if_match=if_match, opc_client_request_id=ctx.obj['request_id']))


objectstorage.add_command(bucket)
bucket.add_command(bucket_create)
bucket.add_command(bucket_list)
bucket.add_command(bucket_get)
bucket.add_command(bucket_delete)
bucket.add_command(bucket_update)


@click.group('object')
@help_option_group
def object_group():
    pass


@click.command(name='list')
@click.option('-ns', '--namespace', required=True, help='The top-level namespace used for the request.')
@click.option('-bn', '--bucket-name', required=True, help='The name of the bucket.')
@click.option('--prefix', help='Only object names that begin with this prefix will be returned.')
@click.option('--start', help='Only object names greater or equal to this parameter will be returned.')
@click.option('--end', help='Only object names less than this parameter will be returned.')
@click.option('--limit', default=100, show_default=True, help='The maximum number of items to return.')
@click.option('--delimiter', help="When this parameter is set, only objects whose names do not contain the "
                                  "delimiter character (after an optionally specified prefix) are returned. "
                                  "Scanned objects whose names contain the delimiter have part of their name "
                                  "up to the last occurrence of the delimiter (after the optional prefix) "
                                  "returned as a set of prefixes. Note: Only '/' is a supported delimiter "
                                  "character at this time.")
@click.option('--fields', default='name,size,timeCreated,md5', show_default=True,
              help="Object summary in list of objects includes the 'name' field. This parameter may also include "
                   "'size' (object size in bytes), 'md5', and 'timeCreated' (object creation date and time) fields. "
                   "Value of this parameter should be a comma separated, case-insensitive list of those field names.")
@help_option
@click.pass_context
@wrap_exceptions
def object_list(ctx, namespace, bucket_name, prefix, start, end, limit, delimiter, fields):
    """
    Lists the objects in a bucket.

    Example:
        bmcs os object list -ns mynamespace -bn mybucket --fields name,size,timeCreated
    """

    client = build_client('os', ctx)

    args = {
        'fields': fields,
        'opc_client_request_id': ctx.obj['request_id']
    }
    if start:
        args['start'] = start

    if delimiter is not None:
        args['delimiter'] = delimiter

    if end is not None:
        args['end'] = end

    if prefix is not None:
        args['prefix'] = prefix

    all_objects = []
    prefixes = list()

    while limit > 0:

        args['limit'] = min(limit, OBJECT_LIST_PAGE_SIZE)

        response = client.list_objects(
            namespace,
            bucket_name,
            **args
        )

        if response.data.prefixes is not None:
            for prefix in response.data.prefixes:
                if prefix not in prefixes:
                    prefixes.append(prefix)

        objects = response.data.objects
        next_start = response.data.next_start_with

        all_objects.extend(objects)

        if next_start:
            limit -= len(objects)
            args['start'] = next_start
        else:
            limit = 0

    metadata = {'prefixes': prefixes}

    if response.data.next_start_with:
        metadata['next-start-with'] = response.data.next_start_with

    render(all_objects, metadata, display_all_headers=True)


@click.command(name='put')
@click.option('-ns', '--namespace', required=True, help='The top-level namespace used for the request.')
@click.option('-bn', '--bucket-name', required=True, help='The name of the bucket.')
@click.option('--file', required=True, type=click.File(mode='rb'),
              help="The file to load as the content of the object, or '-' to read from STDIN.")
@click.option('--name',
              help='The name of the object. Default value is the filename excluding the path. Required if reading object from STDIN.')
@click.option('--if-match', help='The entity tag to match.')
@click.option('--content-md5', help='The base-64 encoded MD5 hash of the body.')
@click.option('--metadata', help='Arbitrary string keys and values for user-defined metadata. Must be in JSON format. Example: \'{"key1":"value1","key2":"value2"}\'')
@click.option('--content-type', help='The content type of the object.')
@click.option('--content-language', help='The content language of the object.')
@click.option('--content-encoding', help='The content encoding of the object.')
@click.option('--force', is_flag=True, help='If the object already exists, overwrite the existing object without a confirmation prompt.')
@click.option('--no-multipart', is_flag=True,
              help='Do not use multipart uploads to upload the file in parts. By default files above 128 MiB will be uploaded in multiple parts, then combined server-side.')
@click.option('--part-size', type=int,
              help='Part size (in MiB) to use if uploading via multipart upload operations')
@help_option
@click.pass_context
@wrap_exceptions
def object_put(ctx, namespace, bucket_name, name, file, if_match, content_md5, metadata, content_type, content_language, content_encoding, force, no_multipart, part_size):
    """
    Creates a new object or overwrites an existing one.

    Example:
        bmcs os object put -ns mynamespace -bn mybucket --name myfile.txt --file /Users/me/myfile.txt --metadata '{"key1":"value1","key2":"value2"}'
    """
    client = build_client('os', ctx)

    client_request_id = ctx.obj['request_id']
    kwargs = {'opc_client_request_id': client_request_id}

    # default object name is filename without path
    if not name:
        if not hasattr(file, 'name') or file.name == '<stdin>':
            raise click.UsageError('Option "--name" must be provided when reading object from stdin')

        name = os.path.basename(file.name)

    if part_size is not None and no_multipart:
        raise click.UsageError('The option --part-size is not applicable when using the --no-multipart flag.')

    if not force:
        etag = get_object_etag(client, namespace, bucket_name, name, client_request_id, if_match)

        if etag is None:
            # Object does not exist, so make sure that the put fails if one is created in the meantime.
            kwargs['if_none_match'] = '*'
        else:
            kwargs['if_match'] = etag
            if not click.confirm("WARNING: This object already exists. Are you sure you want to overwrite it?"):
                ctx.abort()

    if if_match is not None:
        kwargs['if_match'] = if_match

    if content_md5 is not None:
        kwargs['content_md5'] = content_md5

    if metadata is not None:
        kwargs['metadata'] = parse_json_parameter("metadata", metadata, default={})

    if content_type is not None:
        kwargs['content_type'] = content_type

    if content_language is not None:
        kwargs['content_language'] = content_language

    if content_encoding is not None:
        kwargs['content_encoding'] = content_encoding

    # Force UploadManager to not use multipart if the client does not want it or
    # if the stream is coming from stdin.
    if no_multipart or file.name == '<stdin>':
        kwargs['no_multipart'] = True

    if part_size is not None:
        kwargs['part_size'] = part_size * MEBIBYTE

    total_size = os.fstat(file.fileno()).st_size
    if total_size > 0:
        # TODO: Provide a way of updating the progress without coupling UploadManager to
        # click's progress bar.
        progress = Progress('')
        with ProgressBar(total_size, '', progress.get_label) as bar:
            progress.set_bar(bar)
            kwargs['progress'] = progress
            response = UploadManager.upload(client, namespace, bucket_name, name, file, **kwargs)
    else:
        response = UploadManager.upload(client, namespace, bucket_name, name, file, **kwargs)
    display_headers = filter_object_headers(response.headers, OBJECT_PUT_DISPLAY_HEADERS)
    render(None, display_headers, display_all_headers=True)


def get_object_etag(client, namespace, bucket_name, name, client_request_id, if_match):
    """Returns the etag for the specified object, or None if it doesn't exist."""
    kwargs = {'opc_client_request_id': client_request_id}
    etag = None

    if if_match is not None:
        kwargs['if_match'] = if_match
    try:
        response = client.head_object(namespace, bucket_name, name, **kwargs)
        etag = response.headers['etag']
    except exceptions.ServiceError as e:
        if e.status != 404:
            raise

    return etag


@click.command(name='get')
@click.option('-ns', '--namespace', required=True, help='The top-level namespace used for the request.')
@click.option('-bn', '--bucket-name', required=True, help='The name of the bucket.')
@click.option('--name', required=True, help='The name of the object.')
@click.option('--file', required=True, type=click.File(mode='wb'),
              help="The name of the file that will receive the object content, or '-' to write to STDOUT.")
@click.option('--if-match', help='The entity tag to match.')
@click.option('--if-none-match', help='The entity tag to avoid matching.')
@click.option('--range',
              help='Byte range to fetch. Follows https://tools.ietf.org/html/rfc7233#section-2.1. Example: bytes=2-10')
@help_option
@click.pass_context
@wrap_exceptions
def object_get(ctx, namespace, bucket_name, name, file, if_match, if_none_match, range):
    """
    Gets the metadata and body of an object.

    Example:
        bmcs os object get -ns mynamespace -bn mybucket --name myfile.txt --file /Users/me/myfile.txt
    """
    client = build_client('os', ctx)
    response = client.get_object(
        namespace,
        bucket_name,
        name,
        if_match=if_match,
        if_none_match=if_none_match,
        range=range,
        opc_client_request_id=ctx.obj['request_id']
    )

    # if outputting to stdout we don't want to print a progress bar because it will get mixed up with the output
    bar = None
    if hasattr(file, 'name') and file.name != '<stdout>':
        bar = ProgressBar(total_bytes=int(response.headers['Content-Length']), label='Downloading object')

    # Stream using the raw urllib3.HTTPResponse, since using the Requests response
    # will automatically try to decode.
    for chunk in response.data.raw.stream(OBJECT_GET_CHUNK_SIZE, decode_content=False):
        if bar:
            bar.update(len(chunk))
        file.write(chunk)

    if bar:
        bar.render_finish()


@click.command(name='head')
@click.option('-ns', '--namespace', required=True, help='The top-level namespace used for the request.')
@click.option('-bn', '--bucket-name', required=True, help='The name of the bucket.')
@click.option('--name', required=True, help='The name of the object.')
@click.option('--if-match', help='The entity tag to match.')
@click.option('--if-none-match', help='The entity tag to avoid matching.')
@help_option
@click.pass_context
@wrap_exceptions
def object_head(ctx, namespace, bucket_name, name, if_match, if_none_match):
    """
    Gets the user-defined metadata and entity tag for an object.

    Example:
        bmcs os object head -ns mynamespace -bn mybucket --name myfile.txt
    """
    client = build_client('os', ctx)
    response = client.head_object(
        namespace,
        bucket_name,
        name,
        if_match=if_match,
        if_none_match=if_none_match,
        opc_client_request_id=ctx.obj['request_id'])

    render(None, response.headers, display_all_headers=True)


@click.command(name='delete')
@click.option('-ns', '--namespace', required=True, help='The top-level namespace used for the request.')
@click.option('-bn', '--bucket-name', required=True, help='The name of the bucket.')
@click.option('--name', required=True, help='The name of the object to delete.')
@click.option('--if-match', help='The entity tag to match.')
@confirm_delete_option
@help_option
@click.pass_context
@wrap_exceptions
def object_delete(ctx, namespace, bucket_name, name, if_match):
    """
    Deletes an object.

    Example:
        bmcs os object delete -ns mynamespace -bn mybucket --name myfile.txt
    """
    client = build_client('os', ctx)
    render_response(client.delete_object(namespace, bucket_name, name, if_match=if_match, opc_client_request_id=ctx.obj['request_id']))


@click.command(name='resume-put')
@click.option('-ns', '--namespace', required=True, help='The top-level namespace used for the request.')
@click.option('-bn', '--bucket-name', required=True, help='The name of the bucket.')
@click.option('--file', required=True, type=click.File(mode='rb'),
              help="The file to load as the content of the object.")
@click.option('--name',
              help='The name of the object. Default value is the filename excluding the path.')
@click.option('--upload-id', required=True, help='Upload ID to resume.')
@click.option('--part-size', type=int,
              help='Part size in MiB')
@help_option
@click.pass_context
@wrap_exceptions
def object_resume_put(ctx, namespace, bucket_name, name, file, upload_id, part_size):
    """
    Resume a previous multipart put.

    Example:
        bmcs os object resume-put -ns mynamespace -bn mybucket --name myfile.txt --file /Users/me/myfile.txt --upload-id my-upload-id
    """
    kwargs = {}

    if part_size is not None:
        kwargs['part_size'] = part_size * MEBIBYTE

    # Don't accept stdin with resume-put
    if file.name == '<stdin>':
        raise click.UsageError('Stdin is not supported by resume-put')

    # default object name is filename without path
    if not name:
        if not hasattr(file, 'name'):
            raise click.UsageError('The --file must have a name attribute, or --name must be specified')
        name = os.path.basename(file.name)

    client = build_client('os', ctx)

    total_size = os.fstat(file.fileno()).st_size
    if total_size > 0:
        progress = Progress('')
        with ProgressBar(total_size, '', progress.get_label) as bar:
            progress.set_bar(bar)
            kwargs['progress'] = progress
            response = UploadManager.resume(client, namespace, bucket_name, name, file, upload_id, **kwargs)

        display_headers = filter_object_headers(response.headers, OBJECT_PUT_DISPLAY_HEADERS)
        render(None, display_headers, display_all_headers=True)


objectstorage.add_command(object_group)
object_group.add_command(object_list)
object_group.add_command(object_put)
object_group.add_command(object_get)
object_group.add_command(object_head)
object_group.add_command(object_delete)
object_group.add_command(object_resume_put)


@click.group(name='multipart')
@help_option_group
def multipart():
    pass


@click.command(name='list')
@click.option('-ns', '--namespace', required=True, help='The top-level namespace used for the request.')
@click.option('-bn', '--bucket-name', required=True, help='The name of the bucket.')
@click.option('--limit', default=100, type=int, show_default=True, help='The maximum number of items to return.')
@click.option('--page', help="""The value of the `opc-next-page` response header from the previous \"List\" call.""")
@help_option
@click.pass_context
@wrap_exceptions
def multipart_list(ctx, namespace, bucket_name, limit, page):
    """
    List uncommitted multipart uploads for a namespace and bucket

    Example:
        bmcs os multipart list -ns mynamespace -bn mybucket
    """
    client = build_client('os', ctx)

    args = {
        'opc_client_request_id': ctx.obj['request_id'],
        'limit': limit
    }

    if page:
        args['page'] = page

    render_response(client.list_multipart_uploads(namespace, bucket_name, **args))


@click.command(name='abort')
@click.option('-ns', '--namespace', required=True, help='The top-level namespace used for the request.')
@click.option('-bn', '--bucket-name', required=True, help='The name of the bucket.')
@click.option('-on', '--object-name', required=True, help='The name of the object.')
@click.option('--upload-id', required=True, help='Upload ID to abort.')
@click.option('--force', is_flag=True, help='Abort the existing multipart upload without a confirmation prompt.')
@help_option
@click.pass_context
@wrap_exceptions
def multipart_abort(ctx, namespace, bucket_name, object_name, upload_id, force):
    """
    Aborts an uncommitted multipart upload

    Example:
        bmcs os multipart abort -ns mynamespace -bn mybucket --name myfile.txt --upload-id my-upload-id
    """
    client = build_client('os', ctx)

    if not force:
        try:
            response = client.list_multipart_upload_parts(namespace, bucket_name, object_name, upload_id, limit=1)
            render_response(response)
            if response.status == 200:
                if not click.confirm("WARNING: Are you sure you want to permanently remove this incomplete upload?"):
                    ctx.abort()
        except exceptions.ServiceError as e:
            if e.status != 404:
                raise

    render_response(client.abort_multipart_upload(namespace, bucket_name, object_name, upload_id))


objectstorage.add_command(multipart)
multipart.add_command(multipart_list)
multipart.add_command(multipart_abort)


class FileReadCallbackStream:
    def __init__(self, file, progress_callback):
        self.progress_callback = progress_callback
        self.file = file
        self.mode = file.mode

    # this is used by 'requests' to determine the Content-Length header using fstat
    def fileno(self):
        return self.file.fileno()

    def read(self, n):
        self.progress_callback(n)
        return self.file.read(n)


class Progress:
    def __init__(self, label):
        self.label = label
        self.bar = None

    def set_bar(self, bar):
        self.bar = bar

    def update(self, count):
        self.bar.update(count)

    def get_label(self, current_item):
        return self.label


class ProgressBar:
    PROGRESS_BAR_GRANULARITY = 10000

    def __init__(self, total_bytes, label, next_part=None):
        self._total_bytes = total_bytes
        self._total_progress_bytes = 0
        self._last_progress = 0
        self._progressbar = click.progressbar(length=ProgressBar.PROGRESS_BAR_GRANULARITY,
                                              label=label, file=sys.stderr, item_show_func=next_part)

    def __enter__(self):
        self._progressbar.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self._progressbar.__exit__(exc_type, exc_value, tb)

    def update(self, bytes_read):
        self._total_progress_bytes += bytes_read
        current_progress = ProgressBar.PROGRESS_BAR_GRANULARITY * (float(self._total_progress_bytes) / self._total_bytes)
        if current_progress != self._last_progress:
            self._progressbar.update(current_progress - self._last_progress)
            self._last_progress = current_progress

    def render_finish(self):
        self._progressbar.render_finish()
