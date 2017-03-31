"""Download and upload of EAC-CPF data."""

from __future__ import print_function

from . import _oai_save_records


def fetch_eac_records(url, output, **kwargs):
    """Retrieve EAC records through OAI-PMH."""
    _oai_save_records(output, url, 'eac', 'authorityrecord', **kwargs)


def upload_eac(url, file, credentials_file=None, verbose=False):
    """POST an EAC XML file to the referential using dedicated web service."""
    # pylint: disable=too-many-locals, redefined-builtin
    import yaml
    import requests
    from cwclientlib.cwproxy import SignedRequestAuth, CWProxy, build_request_headers

    if credentials_file is None:
        credentials_file = 'cubicweb.yaml'
    if verbose:
        print('reading credentials from', credentials_file)
    with open(credentials_file) as stream:
        credentials = yaml.load(stream)
    if not isinstance(credentials, dict):
        raise Exception('{} is not correctly formatted, a dictionary is expected'
                        .format(credentials_file))
    if not ('id' in credentials and 'secret' in credentials):
        raise Exception('{} is missing id or secret'.format(credentials_file))

    auth = SignedRequestAuth(credentials['id'], credentials['secret'])
    proxy = CWProxy(url, auth, verify=False)

    headers = build_request_headers()
    headers['Content-Type'] = 'application/xml'
    # XXX copy of CWProxy.post().
    params = {
        'url': proxy.build_url('/authorityrecord'),
        'headers': headers,
        'verify': proxy._ssl_verify,  # pylint: disable=protected-access
        'auth': proxy.auth,
    }
    if proxy.timeout:
        params['timeout'] = proxy.timeout

    if verbose:
        print('posting {} to {}'.format(file, url))
    with open(file) as infile:
        params['data'] = infile.read()
        response = requests.post(**params)

    print(response.json())
