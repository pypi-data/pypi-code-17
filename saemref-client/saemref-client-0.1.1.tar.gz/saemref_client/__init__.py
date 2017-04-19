"""Interact with a SAEM-Ref server."""

from __future__ import print_function

import os
from os import path

import iso8601


def _oai_client(url, prefix):
    from oaipmh.client import Client
    from oaipmh.metadata import MetadataRegistry, MetadataReader

    registry = MetadataRegistry()
    registry.registerReader(prefix, MetadataReader)
    if not url.endswith('/'):
        url += '/'
    url += 'oai'
    return Client(url, registry)


# pylint: disable=too-many-locals, too-many-arguments
def _oai_save_records(outdir, url, metadata_prefix, setspec,
                      from_date=None, until_date=None, limit=None, verbose=False):
    """List records using OAI-PMH and save the as XML files in `outdir`."""
    from lxml import etree

    client = _oai_client(url, metadata_prefix)
    records = client.listRecords(metadataPrefix=metadata_prefix, set=setspec,
                                 from_=from_date, until=until_date)

    for idx, (header, reader, _) in enumerate(records):
        identifier = header.identifier()
        what, name = identifier.rsplit('/')[-2:]
        fname = '{0}_{1}.xml'.format(what, name)
        fpath = path.join(outdir, fname)
        if verbose:
            print('saving {0} to {1}'.format(identifier, fpath))
        tree = etree.ElementTree(reader._fields[0])
        with open(fpath, 'wb') as outfile:
            tree.write(outfile)
        if limit is not None and idx == limit:
            break


def _add_generic_arguments(parser):
    parser.add_argument('url', help='base URL of the SAEM-Ref instance')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='display progress information')


def _parse_date(datestr):
    """Parse an iso8601 date into a naive datetime."""
    datetime = iso8601.parse_date(datestr, default_timezone=None)
    return datetime.replace(tzinfo=None)


def _add_oai_arguments(parser):
    _add_generic_arguments(parser)
    parser.add_argument('-o', '--output', default=os.getcwd(),
                        help='output directory (default to current directory)')
    parser.add_argument('--from',
                        help='fetch records from this date (ISO 8601 datestamp)',
                        type=_parse_date, dest='from_date')
    parser.add_argument('--until',
                        help='fetch records until this date (ISO 8601 datestamp)',
                        type=_parse_date, dest='until_date')
    parser.add_argument('--limit', type=int,
                        help='fetch at much LIMIT records')


def main():
    """CLI entry point."""
    from argparse import ArgumentParser
    from .eac import fetch_eac_records, upload_eac
    from .skos import fetch_concepts

    parser = ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers()

    eac_parser = subparsers.add_parser(
        'eac-download', help='download EAC-CPF authority records')
    eac_parser.set_defaults(func=fetch_eac_records)
    _add_oai_arguments(eac_parser)

    skos_parser = subparsers.add_parser(
        'skos-download', help='download a SKOS concept scheme')
    skos_parser.set_defaults(func=fetch_concepts)
    _add_oai_arguments(skos_parser)
    skos_parser.add_argument(
        'scheme', help='identifier of the concept scheme')

    eac_upload = subparsers.add_parser(
        'eac-upload', help='upload an EAC-CPF file')
    eac_upload.set_defaults(func=upload_eac)
    _add_generic_arguments(eac_upload)
    eac_upload.add_argument(
        'file', help='file path of the EAC-CPF file to upload')
    eac_upload.add_argument('--credentials-file', default='cubicweb.yaml',
                            help='credentials file, '
                            'should contains values for "id" and "secret"')

    args = parser.parse_args()
    func = args.func
    del args.func
    func(**vars(args))
