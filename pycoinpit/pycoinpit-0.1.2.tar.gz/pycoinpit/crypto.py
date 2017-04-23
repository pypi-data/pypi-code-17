import hashlib
import hmac
import binascii
import pybitcointools
import pyelliptic


def get_headers(user_id, shared_secret, nonce, method, uri, body=None):
    request_string = '{"method":"' + method + '","uri":"' + uri + (
    '",' if (body == None) else '","body":' + body + ',') + '"nonce":' + nonce + '}'
    mac = hmac.new(shared_secret, request_string, hashlib.sha256)
    sig = mac.hexdigest()
    headers = {
        'Authorization': 'HMAC ' + user_id + ':' + sig,
        'Nonce'        : nonce,
        'Accept'       : 'application/json'
    }
    return headers


def get_shared_secret(server_pub_key, private_key):
    user_pub_key = get_pub_key(private_key)
    network_code = get_network_code(private_key)
    uncompressed_user_key = binascii.unhexlify(pybitcointools.decompress(user_pub_key))
    uncompressed_server_key = binascii.unhexlify(pybitcointools.decompress(server_pub_key))
    user_priv_key_bin = binascii.unhexlify(pybitcointools.encode_privkey(private_key, 'hex', network_code))
    user = pyelliptic.ECC(privkey=user_priv_key_bin, pubkey=uncompressed_user_key, curve='secp256k1')
    shared_secret = user.get_ecdh_key(uncompressed_server_key)
    return shared_secret


def get_pub_key(private_key):
    return pybitcointools.privtopub(private_key)


def get_user_id(user_pub_key, network_code):
    return pybitcointools.pubtoaddr(user_pub_key, network_code)


def get_network_code(private_key):
    if (private_key[0] == 'K' or private_key[0] == 'L'):
        network_code = 0
    else:
        network_code = 111
    return network_code
