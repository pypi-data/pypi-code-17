from __future__ import unicode_literals

from os.path import basename
import argparse
import datetime
import getpass
import hashlib
import json
import socket
import sys

from jsonschema.exceptions import ValidationError
import jsonschema
import yaml

from . import doc_split, usage, version
from .transfer_client import TransferClient


def _write(output_handle, data):
    output_handle.write('{}\n'.format(json.dumps(data, indent=4)))


def users(output_handle, server_name, user_id, ssl_check):
    """Gives a JSON object of a user together with its transfers.

    :arg stream output_handle: Open writeable handle to a file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    _write(
        output_handle, TransferClient(server_name, ssl_check).users(user_id))


def schema(output_handle, server_name, user_id, ssl_check):
    """Gives the JSON schema for a user.

    :arg stream output_handle: Open writeable handle to a file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    _write(
        output_handle, TransferClient(server_name, ssl_check).schema(user_id))


def transfers(output_handle, metadata_handle, server_name, user_id, ssl_check):
    """Initiates a new transfer.

    :arg stream output_handle: Open writeable handle to a file.
    :arg stream metadata_handle: Open readable handle to a metadata file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    _write(output_handle, TransferClient(server_name, ssl_check).transfers(
        user_id, json.loads(metadata_handle.read()), metadata_handle.name))


def status(output_handle, server_name, user_id, transfer_id, ssl_check):
    """Gives a JSON object of a transfer.

    :arg stream output_handle: Open writeable handle to a file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg str transfer_id: Transfer ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    _write(output_handle, TransferClient(server_name, ssl_check).status(
        user_id, transfer_id))


def update(
        output_handle, server_name, user_id, transfer_id, status, ssl_check):
    """Updates a transfer.

    :arg stream output_handle: Open writeable handle to a file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg str transfer_id: Transfer ID.
    :arg str status: Transfer status.
    :arg bool ssl_check: Check server SSL certificate.
    """
    _write(output_handle, TransferClient(server_name, ssl_check).update(
        user_id, transfer_id, status))


def uploads(
        output_handle, file_handle, server_name, user_id, transfer_id,
        ssl_check):
    """Uploads a file to a transfer.

    :arg stream output_handle: Open writeable handle to a file.
    :arg stream file_handle: Open readable handle to a file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg str transfer_id: Transfer ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    _write(output_handle, TransferClient(server_name, ssl_check).uploads(
        user_id, transfer_id, file_handle))


def completed(output_handle, server_name, client_id, ssl_check):
    """Gives a JSON object of all transfers for this client, i.e., a list of
    transfer ids.

    :arg stream output_handle: Open writeable handle to a file.
    :arg str server_name: Name of the transfer server.
    :arg str client_id: Client ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    _write(
        output_handle,
        TransferClient(server_name, ssl_check).completed(client_id))


def _minimal_metadata(title):
    return {'title': title, 'files': []}


def _make_metadata(log_handle, file_handles, title):
    """Given a list of files, generate the metadata according to the minimal
    transfer metadata schema.

    :arg stream log_handle: Open writeable handle to a file.
    :arg list file_handles: List of open readable file handles.
    :arg str title: Transfer title.

    :returns dict: Metadata in JSON format.
    """
    metadata = _minimal_metadata(title)

    for file_handle in file_handles:
        log_handle.write(
            'Calculating checksum for file: {}.\n'.format(file_handle.name))
        hash_sum = hashlib.md5()
        for chunk in iter(lambda: file_handle.read(4096), b''):
            hash_sum.update(chunk)
        file_handle.seek(0)

        metadata['files'].append({
            'filename': basename(file_handle.name),
            'md5': hash_sum.hexdigest()})

    return metadata


def make_metadata(output_handle, log_handle, file_handles, title):
    """Given a list of files, generate the metadata according to the minimal
    transfer metadata schema.

    :arg stream output_handle: Open writeable handle to a file.
    :arg stream log_handle: Open writeable log to a file.
    :arg list file_handles: List of open readable file handles.
    :arg str title: Transfer title.
    """
    _write(output_handle, _make_metadata(log_handle, file_handles, title))


def _metadata_bailout_dialogue(log_handle, error, metadata):
    """Interactive dialogue for saving metadata.

    :arg stream log_handle: Open writeable log to a file.
    :arg Exception error: Exception.
    :arg dict metadata: Metadata.
    """
    log_handle.write('Error: {}\n\n'.format(str(error)))
    save_metadata = raw_input('Save metadata for future use (Y/n)? ')
    if save_metadata != 'n':
        file_name = raw_input('Please provide a filename: ')
        if file_name:
            _write(open(file_name, 'w'), metadata)


def transfer(log_handle, file_handles, server_name, user_id, title, ssl_check):
    """Transfer a list of files.

    :arg stream log_handle: Open writeable log to a file.
    :arg list file_handles: List of open readable file handles.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg str title: Transfer title.
    :arg bool ssl_check: Check server SSL certificate.
    """
    transfer_client = TransferClient(server_name, ssl_check)

    # Sanity check before we do anything.
    test_metadata = _minimal_metadata('title')
    test_metadata['files'].append(
        {'filename': 'file', 'md5': '00000000000000000000000000000000'})
    jsonschema.validate(test_metadata, transfer_client.schema(user_id))

    # Make the metadata and transfer the files.
    metadata = _make_metadata(log_handle, file_handles, title)
    try:
        transfer_id = transfer_client.transfers(
            user_id, metadata, 'metadata.json')['id']
    except (ValueError, OSError, IOError) as error:
        _metadata_bailout_dialogue(log_handle, error, metadata)
        return
    log_handle.write('Transfer ID: {}.\n'.format(transfer_id))
    for file_handle in file_handles:
        log_handle.write('Uploading file: {}.\n'.format(file_handle.name))
        transfer_client.uploads(user_id, transfer_id, file_handle)


def _interrupted_transfer(log_handle, transfer_client, user_id):
    """Find an interrupted transfer.

    :arg stream log_handle: Open writeable log to a file.
    :arg object transfer_client: Transfer client class instance.
    :arg str user_id: User ID.

    :returns dict: Interrupted transfer object in JSON format.
    """
    transfers = transfer_client.users(user_id)['transfers']

    if not (transfers and transfers[-1]['status'] == 'initiated'):
        raise ValueError('no interrupted transfers found')

    transfer = transfers[-1]
    log_handle.write('Transfer ID: {}.\n'.format(transfer['id']))

    return transfer


def resume(log_handle, server_name, user_id, ssl_check):
    """Resume an interrupted transfer.

    :arg stream log_handle: Open writeable log to a file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    transfer_client = TransferClient(server_name, ssl_check)

    transfer = _interrupted_transfer(log_handle, transfer_client, user_id)
    for file_object in transfer['files']:
        if file_object['status'] == 'pending':
            log_handle.write(
                'Uploading file: {}.\n'.format(file_object['filename']))
            with open(file_object['filename'], 'rb') as file_handle:
                transfer_client.uploads(user_id, transfer['id'], file_handle)


def cancel(log_handle, server_name, user_id, ssl_check):
    """Cancel an interrupted transfer.

    :arg stream log_handle: Open writeable log to a file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    transfer_client = TransferClient(server_name, ssl_check)

    transfer = _interrupted_transfer(log_handle, transfer_client, user_id)
    transfer_client.update(user_id, transfer['id'], 'cancelled')


def _write_yaml(output_handle, data):
    output_handle.write(yaml.safe_dump(
        data, width=76, default_flow_style=False,
        allow_unicode=True).decode('utf-8'))


def _read_timestamp(timestamp):
    return datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')


def _reformat_transfer(transfer):
    """Reformat a transfer object for human readability.

    :arg object transfer: Transfer object.

    :returns dict: Reformatted transfer object in JSON format.
    """
    readable_transfer = transfer.copy()

    files = readable_transfer.pop('files')
    readable_transfer['number_of_files'] = len(files)

    if readable_transfer['status'] == 'initiated':
        readable_transfer['uploaded'] = len(
            filter(lambda x: x['status'] == 'uploaded', files))

    if 'end_date' in readable_transfer:
        readable_transfer['duration'] = str(
            _read_timestamp(readable_transfer['end_date']) -
            _read_timestamp(readable_transfer['start_date']))

    return readable_transfer


def transfers_summary(output_handle, server_name, user_id, ssl_check):
    """Give a human readable summary of all transfers.

    :arg stream output_handle: Open writeable handle to a file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    transfer_client = TransferClient(server_name, ssl_check)

    _write_yaml(
        output_handle,
        map(_reformat_transfer, transfer_client.users(user_id)['transfers']))


def last_transfer_summary(output_handle, server_name, user_id, ssl_check):
    """Give a human readable summary of the last transfer.

    :arg stream output_handle: Open writeable handle to a file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    transfer_client = TransferClient(server_name, ssl_check)

    transfers = transfer_client.users(user_id)['transfers']
    if transfers:
        _write_yaml(output_handle, _reformat_transfer(transfers[-1]))


def transfer_summary(
        output_handle, server_name, user_id, transfer_id, ssl_check):
    """Give a human readable summary of a transfer.

    :arg stream output_handle: Open writeable handle to a file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg str transfer_id: Transfer ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    transfer_client = TransferClient(server_name, ssl_check)

    for transfer in transfer_client.users(user_id)['transfers']:
        if transfer['id'] == transfer_id:
            _write_yaml(output_handle, transfer)
            break


def check_metadata(metadata_handle, server_name, user_id, ssl_check):
    """Check a metadata file against the JSON schema.

    :arg stream metadata_handle: Open readable handle to a metadata file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    jsonschema.validate(
        json.loads(metadata_handle.read()),
        TransferClient(server_name, ssl_check).schema(user_id))


def main():
    """Main entry point.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=usage[0], epilog=usage[1])
    parser.add_argument('-v', action='version', version=version(parser.prog))
    subparsers = parser.add_subparsers(dest='subcommand')

    server_name_parser = argparse.ArgumentParser(add_help=False)
    server_name_parser.add_argument(
        'server_name', metavar='SERVER', type=str, help='server name')

    user_id_parser = argparse.ArgumentParser(add_help=False)
    user_id_parser.add_argument(
        'user_id', metavar='USER', type=str, help='user id')

    transfer_id_parser = argparse.ArgumentParser(add_help=False)
    transfer_id_parser.add_argument(
        'transfer_id', metavar='TRANSFER', type=str, help='transfer id')

    output_parser = argparse.ArgumentParser(add_help=False)
    output_parser.add_argument(
        '-o', dest='output_handle', metavar='OUTPUT',
        type=argparse.FileType('w'), default=sys.stdout, help='output file')

    files_parser = argparse.ArgumentParser(add_help=False)
    files_parser.add_argument(
        'file_handles', metavar='FILE', type=argparse.FileType('rb'),
        nargs='+', help='files to be transferred')

    title_parser = argparse.ArgumentParser(add_help=False)
    title_parser.add_argument(
        '-t', dest='title', type=str,
        default='Transfer from {} by {} using {}'.format(
            socket.gethostname(), getpass.getuser(), parser.prog),
        help='transfer title (default="%(default)s")')

    ssl_parser = argparse.ArgumentParser(add_help=False)
    ssl_parser.add_argument(
        '-n', dest='ssl_check', default=True, action='store_false',
        help='disable SSL certificate check')

    metadata_parser = argparse.ArgumentParser(add_help=False)
    metadata_parser.add_argument(
        'metadata_handle', metavar='METADATA', type=argparse.FileType('r'),
        help='metadata file')

    log_parser = argparse.ArgumentParser(add_help=False)
    log_parser.add_argument(
        '-l', dest='log_handle', metavar='LOG',
        type=argparse.FileType('w'), default=sys.stderr, help='log file')

    default_parser = argparse.ArgumentParser(
        add_help=False,
        parents=[output_parser, server_name_parser, user_id_parser,
            ssl_parser])

    default_verbose_parser = argparse.ArgumentParser(
        add_help=False,
        parents=[log_parser, server_name_parser, user_id_parser, ssl_parser])

    subparser = subparsers.add_parser(
        'users', parents=[default_parser],
        description=doc_split(users))
    subparser.set_defaults(func=users)

    subparser = subparsers.add_parser(
        'schema', parents=[default_parser],
        description=doc_split(schema))
    subparser.set_defaults(func=schema)

    subparser = subparsers.add_parser(
        'transfers',
        parents=[default_parser, metadata_parser],
        description=doc_split(transfers))
    subparser.set_defaults(func=transfers)

    subparser = subparsers.add_parser(
        'status', parents=[default_parser, transfer_id_parser],
        description=doc_split(status))
    subparser.set_defaults(func=status)

    subparser = subparsers.add_parser(
        'update', parents=[default_parser, transfer_id_parser],
        description=doc_split(update))
    subparser.add_argument(
        'status', metavar='STATUS', choices=['cancelled'],
        help='transfer status (choose from: {%(choices)s})')
    subparser.set_defaults(func=update)

    subparser = subparsers.add_parser(
        'uploads',
        parents=[default_parser, transfer_id_parser],
        description=doc_split(uploads))
    subparser.add_argument(
        'file_handle', metavar='FILE', type=argparse.FileType('rb'),
        help='file to be transferred')
    subparser.set_defaults(func=uploads)

    subparser = subparsers.add_parser(
        'completed', parents=[output_parser, server_name_parser, ssl_parser],
        description=doc_split(completed))
    subparser.add_argument('client_id', metavar='CLIENT',
        type=str, help='client id')
    subparser.set_defaults(func=completed)

    subparser = subparsers.add_parser(
        'make_metadata',
        parents=[output_parser, log_parser, files_parser, title_parser],
        description=doc_split(make_metadata))
    subparser.set_defaults(func=make_metadata)

    subparser = subparsers.add_parser(
        'transfer',
        parents=[default_verbose_parser, files_parser, title_parser],
        description=doc_split(transfer))
    subparser.set_defaults(func=transfer)

    subparser = subparsers.add_parser(
        'resume', parents=[default_verbose_parser],
        description=doc_split(resume))
    subparser.set_defaults(func=resume)

    subparser = subparsers.add_parser(
        'cancel', parents=[default_verbose_parser],
        description=doc_split(cancel))
    subparser.set_defaults(func=cancel)

    subparser = subparsers.add_parser(
        'transfers_summary', parents=[default_parser],
        description=doc_split(transfers_summary))
    subparser.set_defaults(func=transfers_summary)

    subparser = subparsers.add_parser(
        'last_transfer_summary', parents=[default_parser],
        description=doc_split(last_transfer_summary))
    subparser.set_defaults(func=last_transfer_summary)

    subparser = subparsers.add_parser(
        'transfer_summary', parents=[default_parser, transfer_id_parser],
        description=doc_split(transfer_summary))
    subparser.set_defaults(func=transfer_summary)

    subparser = subparsers.add_parser(
        'check_metadata',
        parents=[
            server_name_parser, user_id_parser, ssl_parser, metadata_parser],
        description=doc_split(check_metadata))
    subparser.set_defaults(func=check_metadata)

    try:
        args = parser.parse_args()
    except IOError, error:
        parser.error(error)

    try:
        args.func(
            **{k: v for k, v in vars(args).items()
            if k not in ('func', 'subcommand')})
    except (ValueError, IOError, OSError, ValidationError) as error:
        parser.error(error)


if __name__ == '__main__':
    main()
