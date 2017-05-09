from argparse import ArgumentParser
from sys import exit
import logging
from os import environ, path
from pypif import pif
from citrination_client import CitrinationClient
import json

import stevedore

from pypif.obj.common.license import License
from pypif.obj.common.person import Person


def main():

    if 'CITRINATION_SITE' not in environ:
        site = "https://citrination.com"
    else:
        site = environ['CITRINATION_SITE']
    client = CitrinationClient(environ['CITRINATION_API_KEY'], site)

    parser = ArgumentParser(description="Ingest data files to Citrination")

    # Required:
    parser.add_argument('path',
                        help='Location of the file or directory to import')
    parser.add_argument('format',
                        help='Format of data to import, coresponding to the name of the converter extension')

    # Optional
    parser.add_argument('-d', '--dataset', type=int, default=None, 
                        help='ID of the dataset into which to upload PIFs')
    parser.add_argument('--tags', nargs='+', default=None,
                        help='Tags to add to PIFs')
    parser.add_argument('-l', '--license', default=None,
                        help='License to attach to PIFs (string)')
    parser.add_argument('-c', '--contact', default=None,
                        help='Contact information (string)')
    parser.add_argument('--log', default="WARN", dest="log_level",
                        help='Logging level')
    parser.add_argument('--args', dest="converter_arguments", default={}, type=json.loads,
                        help='Arguments to pass to converter (as JSON dictionary)')

    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    ch = logging.StreamHandler()
    log_number = getattr(logging, args.log_level.upper())
    logger.setLevel(log_number)
    ch.setLevel(log_number)
    logger.addHandler(ch)

    mgr = stevedore.extension.ExtensionManager(
        namespace='citrine.dice.converter',
        invoke_on_load=False
    )

    if args.format in mgr:
        extension = mgr[args.format]
        p = extension.plugin.convert([args.path], **args.converter_arguments)
    else:
        logger.error("Unknown format")
        exit(1)

    if args.tags is not None:
        p.tags = args.tags
    if args.license is not None:
        p.licenses = [License(name=args.license)]
    if args.contact is not None:
        contact = Person()
        toks = args.contact.split()
        email = next(x for x in toks if "@" in x)
        if email is not None:
            contact.email = email.lstrip("<").rstrip(">")
            toks.remove(email)
        contact.name = " ".join(toks)
        p.contacts = [contact]

    if path.isfile(args.path):
        pif_name = path.join(path.dirname(args.path), "pif.json")
    else:
        pif_name = path.join(args.path, "pif.json")

    with open(pif_name, "w") as f:
        pif.dump(p, f, indent=2)
    logger.info("Created pif at {}".format(pif_name))

    if args.dataset:
        if path.isfile(args.path):
            client.upload_file(pif_name, args.dataset)
            logger.info("Uploaded file {}".format(pif_name))
        else:
            client.upload_file(args.path, args.dataset)
            logger.info("Uploaded directory {}".format(args.path))
