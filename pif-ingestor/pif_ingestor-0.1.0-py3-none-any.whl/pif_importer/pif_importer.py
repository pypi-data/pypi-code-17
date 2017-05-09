from argparse import ArgumentParser
import logging
from os import environ, path
from pypif import pif
from citrination_client import CitrinationClient
from dfttopif import directory_to_pif
from pypif.obj.common.license import License
from sparks_pif_converters.DSC import dsc_to_pif
from sparks_pif_converters.LFA import lfa_to_pif
from pypif.obj.common.person import Person


def main():
    client = CitrinationClient(environ['CITRINATION_API_KEY'], 'https://citrination.com')
    parser = ArgumentParser(description="Import data files to Citrination")

    parser.add_argument('dataset', type=int,
                        help='Dataset ID into which to upload PIFs')
    parser.add_argument('path',
                        help='Location of the file or directory to import')
    parser.add_argument('-f', '--format',
                        help='Format of data to import')
    parser.add_argument('--tags', nargs='+', default=None,
                        help='Tags to add to PIFs')
    parser.add_argument('-l', '--license', default=None,
                        help='License to attach to PIFs')
    parser.add_argument('-c', '--contact', default=None,
                        help='Contact information')
    parser.add_argument('--log', default="WARN", dest="log_level",
                        help='Contact information')

    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    ch = logging.StreamHandler()
    log_number = getattr(logging, args.log_level.upper())
    logger.setLevel(log_number)
    ch.setLevel(log_number)
    logger.addHandler(ch)


    if args.format == "VASP":
        logger.info("Parsing as VASP files")
        p = directory_to_pif(args.path, quality_report=True)

    elif args.format == "DSC":
        logger.info("Parsing as DSC files")
        p = dsc_to_pif.netzsch_3500_to_pif(args.path)

    elif args.format == "LFA":
        logger.info("Parsing as LFA files")
        p = lfa_to_pif.lfa457_to_pif(args.path)

    else:
        logger.error("Unknown format")
        return

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

    if path.isfile(args.path):
        client.upload_file(pif_name, args.dataset)
        logger.info("Uploaded file {}".format(pif_name))
    else:
        client.upload_file(args.path, args.dataset, root_path="")
        logger.info("Uploaded directory {}".format(args.path))
