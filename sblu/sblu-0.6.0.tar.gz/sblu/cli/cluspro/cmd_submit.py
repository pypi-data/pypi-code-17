import sys
import logging
import json

import click
import requests

from sblu import CONFIG
from sblu.cli import make_sig

logger = logging.getLogger(__name__)

URL_SCHEME = "https"
API_ENDPOINT = "/api.php"
CP_CONFIG = CONFIG['cluspro']
FORM_KEYS = [
    'username', 'receptor', 'ligand', 'jobname', 'coeffs', 'rotations',
    'antibodymode', 'othersmode', 'masknoncdr'
]
for f in ('pdb', 'chains', 'attraction', 'mask'):
    FORM_KEYS.append("rec" + f)
    FORM_KEYS.append("lig" + f)
FORM_KEYS.append("dssprec")
FORM_KEYS.append("dssplig")
OPTIONAL_FILE_FIELDS = (
    ("coeffs", "coeff_file"),
    ("rotations", "rots_file"),
    ("restraints", "restraints_file"),
    ("saxs_file", "saxs_file"),
    ("recmask", "recrepulsionfile"),
    ("ligmask", "ligrepulsionfile"),
)

@click.command('submit', short_help="Submit a job to ClusPro.")
@click.option("--username", default=CP_CONFIG['username'])
@click.option("--secret", default=CP_CONFIG['api_secret'])
@click.option("--server", default=CP_CONFIG['server'])
@click.option("--coeffs", type=click.Path(exists=True), default=None)
@click.option("--rotations", type=click.Path(exists=True), default=None)
@click.option("-j", "--jobname", help="Optional: will default to job number")
@click.option("-a", "--antibodymode", is_flag=True, default=None)
@click.option("-o", "--othersmode", is_flag=True, default=None)
@click.option("--receptor", type=click.Path(exists=True), help="Upload a PDB file")
@click.option("--ligand", type=click.Path(exists=True), help="Uplaod a PDB file")
@click.option("--recpdb", help="4-letter PDB code")
@click.option("--ligpdb", help="4-letter PDB code")
@click.option("--rec-chains", "recchains", help='chains to use, for example "A B" (in double quotes)')
@click.option("--lig-chains", "ligchains", help='chains to use, for example "A B" (in double quotes)')
@click.option("--rec-mask", "recmask", type=click.Path(exists=True), default=None)
@click.option("--lig-mask", "ligmask", type=click.Path(exists=True), default=None)
@click.option("--rec-attraction", "recattraction", type=click.Path(exists=True), default=None)
@click.option("--lig-attraction", "ligattraction", type=click.Path(exists=True), default=None)
@click.option("--rec-dssp", "dssprec", is_flag=True, default=None)
@click.option("--lig-dssp", "dssplig", is_flag=True, default=None)
@click.option("--restraints", type=click.Path(exists=True), default=None)
@click.option("--saxs-file", type=click.Path(exists=True), default=None)
@click.option("--masknoncdr", is_flag=True, default=None)
def cli(username, secret, server,
        **kwargs):
    if username is None or username == "None" or secret is None or secret == "None":
        if username is None or username == "None":
            username = click.prompt("Please enter your cluspro username")
            CP_CONFIG['username'] = username
        if secret is None or secret == "None":
            secret = click.prompt("Please enter your cluspro api secret")
            CP_CONFIG['api_secret'] = secret
        CONFIG.write()

    if 'receptor' not in kwargs and 'recpdb' not in kwargs:
        raise click.BadOptionUsage("One of --receptor or --recpdb is required")
    if 'ligand' not in kwargs and 'ligpdb' not in kwargs:
        raise click.BadOptionUsage("One of --ligand or --ligpdb is required")

    form = {
        k: v
        for k, v in kwargs.items() if k in FORM_KEYS and v is not None
    }
    form['username'] = username

    files = {}
    if form.get("receptor") is not None:
        files['rec'] = open(form['receptor'], 'rb')
        form['userecpdbid'] = '0'
    else:
        form['userecpdbid'] = '1'
    if form.get("ligand") is not None:
        files['lig'] = open(form['ligand'], 'rb')
        form['useligpdbid'] = '0'
    else:
        form['useligpdbid'] = '1'

    for form_key, files_key in OPTIONAL_FILE_FIELDS:
        if form.get(form_key) is not None:
            files[files_key] = open(form[form_key], 'rb')

    form['sig'] = make_sig(form, secret)

    api_address = "{0}://{1}{2}".format(URL_SCHEME, server, API_ENDPOINT)

    try:
        r = requests.post(api_address, data=form, files=files)
        result = json.loads(r.text)
        if result['status'] == 'success':
            print(result['id'])
        else:
            print(result['errors'])
            sys.exit(1)
    except Exception as ex:
        logger.error("Error submitting job: {}".format(ex))
