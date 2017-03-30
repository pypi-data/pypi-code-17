"""WSGI Auth0 middleware that check for HS256 and RS256 JWT.

Encoded JWT are expected in `Authorizaion` http header, ex::

    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.....

"""
from collections import namedtuple
import logging
import sys

from jose import jwt, jws
from jose.exceptions import JWTError
from jose.utils import base64url_decode
from .exception import Error


PY2 = sys.version_info[0] == 2
log = logging.getLogger(__name__)

Client = namedtuple('Client', 'label id audience secret')
Secret = namedtuple('Secret', 'type value')


def factory(application, config=None, **kwargs):
    monkeypatch_jws_get_keys()
    config = config.copy() if config else {}
    config.update(kwargs)
    app = auth0_middleware(application, config)
    return app


def auth0_middleware(application, config):
    log.info('Setup auth0_middleware')
    log.debug('application=%s config=%s', application, config)

    clients = read_clients(config)

    def app(environ, start_response):
        authorization = environ.get('HTTP_AUTHORIZATION')
        jwt_environ = validate_jwt_claims(clients, authorization)
        environ.update(jwt_environ)
        return application(environ, start_response)

    return app


def validate_jwt_claims(clients, authorization):
    claims = None
    jwt_environ = {}
    if not authorization:
        jwt_environ['JWT_CLAIMS'] = None
        jwt_environ['JWT_AUTH0_CLIENT'] = None
        jwt_environ['JWT_ERROR'] = {
            'code': 'no_authorization',
            'description': 'No authorization in headers.',
        }
    else:
        client = None
        try:
            token = extract_token(authorization)
            client = extract_client(clients, token)
            claims = jwt.decode(
                token,
                client.secret.value,
                audience=client.audience,
            )

        except Error as jwt_error:
            log.debug('Jwt validation error="%r"', jwt_error)
            jwt_environ['JWT_CLAIMS'] = None
            jwt_environ['JWT_ERROR'] = jwt_error.to_dict()
        else:
            jwt_environ['JWT_CLAIMS'] = claims
            jwt_environ['JWT_ERROR'] = None

        if client is not None:
            jwt_environ['JWT_AUTH0_CLIENT'] = client._asdict()
        else:
            jwt_environ['JWT_AUTH0_CLIENT'] = None

        if claims is not None and 'sub' in claims:
            jwt_environ['REMOTE_USER'] = claims['sub']

    log.debug(
        'JWT_ERROR=%s JWT_CLAIMS=%s JWT_AUTH0_CLIENT=%s',
        jwt_environ['JWT_ERROR'],
        jwt_environ['JWT_CLAIMS'],
        jwt_environ['JWT_AUTH0_CLIENT'],
    )

    jwt_environ['wsgiauth0.jwt_claims'] = jwt_environ['JWT_CLAIMS']
    jwt_environ['wsgiauth0.jwt_error'] = jwt_environ['JWT_ERROR']
    jwt_environ['wsgiauth0.jwt_auth0_client'] = jwt_environ['JWT_AUTH0_CLIENT']

    return jwt_environ


def read_clients(config):
    """Load client configuration from all possible sources."""
    client_settings = read_clients_settings(config)
    log.debug('client_settings: %s', client_settings)
    verify_client_settings(client_settings)
    return parse_clients(client_settings)


def read_clients_settings(config):
    """Load client configuration from all possible sources."""
    from .config_yaml import config_yaml
    from .config_dynamodb import config_dynamodb

    client_settings = config.get('clients', {})

    clients = config_yaml(config)
    client_settings.update(clients)

    clients = config_dynamodb(config)
    client_settings.update(clients)

    return client_settings


def verify_client_settings(client_settings):
    if not client_settings:
        raise Error(
            'missing_config',
            "No auth0 clients configured",
        )


def parse_clients(client_settings):
    """Convert input client specs to clients map used for lookup."""
    return {client.label: client
            for client in map(parse_client, client_settings.items())}


def parse_client(item):
    """Convert input client specs to clients map used for lookup."""
    label, client_dict = item
    try:
        secret_type = client_dict['secret']['type']
        secret_value = client_dict['secret']['value']
        client_id = client_dict['id']
        audience = client_dict['audience']
    except (TypeError, KeyError):
        raise Error(
            'missing_config_key',
            'Client config missing key client_dict.',
        )

    if secret_type == 'base64_url_encoded':
        if PY2:
            secret_value = secret_value.encode('utf-8')
        secret_value = base64url_decode(secret_value)

    return Client(
        label=label,
        id=client_id,
        secret=Secret(type=secret_type, value=secret_value),
        audience=audience,
    )


def extract_token(authorization):
    parts = authorization.split()

    if len(parts) != 2:
        raise Error(
            'invalid_header',
            'Authorization header must be "Bearer token".',
        )

    if parts[0].lower() != 'bearer':
        raise Error(
            'invalid_header',
            'Authorization header must start with "Bearer".',
        )

    return parts[1]


def extract_client(clients, token):
    try:
        claims = jwt.get_unverified_claims(token)
    except JWTError:
        raise Error('invalid_token', 'Error decoding token claims.')

    try:
        audience = claims['aud']
    except KeyError:
        raise Error('invalid_claims', 'No key aud in claims.')

    if audience in clients:
        return clients[audience]

    try:
        subject = claims['sub']
    except KeyError:
        raise Error('invalid_claims', 'No key sub in claims.')

    try:
        return clients[subject]
    except KeyError:
        log.debug(
            'No client found for: audience %s, subject %s',
            audience,
            subject,
        )
        raise Error('invalid_client', 'No config found for this client.')


def monkeypatch_jws_get_keys():  # pragma: no cover
    # Monkey patch jws._get_keys to avoid failing with a base64 decoded secret
    original_get_keys = jws._get_keys

    def jws_get_keys(key):
        if isinstance(key, bytes):
            return (key, )
        return original_get_keys(key)

    jws._get_keys = jws_get_keys
