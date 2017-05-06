# -*- coding: utf-8 -*-
""" All input and output parameters are bytestrings, unless specified
otherwise.
"""

from ._recrypto import ffi, lib


def _cstr2bs(charpp):
    """ Convert pointer to a C string into Python's bytestring. Frees
    the C string.
    """
    length = lib.strlen(charpp[0])
    bs = bytes(ffi.buffer(charpp[0][0:length]))
    lib.free(charpp[0])
    return bs


def genprivkey(seed):
    """ Returns a pair (privkey, pubkey)
    """
    ppriv = ffi.new("char **")
    ppub = ffi.new("char **")
    seed = ffi.new("char[]", seed)
    lib.genprivkey(seed, ppriv, ppub)
    return (_cstr2bs(ppriv), _cstr2bs(ppub))


def genpubkey(priv):
    """ Given a private key it generates a matching public key.
    """
    ppriv = ffi.new("char[]", priv)
    ppub = ffi.new("char **")
    lib.genpubkey(ppriv, ppub)
    return _cstr2bs(ppub)


def hashstring(data):
    """ Tiger hash function. Returns a bytestring hex-encoding 192-bit
    hash value.

    Note: this function is weird in how it presents it's result.
    It prints bytes in reversed order, e.g. 0xf0 will become 0f in the
    output string.
    """
    pdata = ffi.new("char[]", data)
    # 192 bits tiger hash in hex + trailing \0
    length = 49
    phash = ffi.new(f"char[{length}]")
    lib.hashstring(pdata, phash, length)
    # don't need the trailing \0 in python
    return bytes(ffi.buffer(phash[0:length-1]))


def answerchallenge(priv, challenge):
    ppriv = ffi.new("char[]", priv)
    pchal = ffi.new("char[]", challenge)
    panswer = ffi.new("char **")
    lib.answerchallenge(ppriv, pchal, panswer)
    return _cstr2bs(panswer)


def parsepubkey(pubstr):
    """ Returns a pubkey object that can be passed to `genchallenge`.
    """
    ppub = ffi.new("char[]", pubstr)
    key = lib.parsepubkey(ppub)
    gckey = ffi.gc(key, lib.freepubkey)
    return gckey


def genchallenge(pubkey, seed):
    """ Returns a pair (correct_answer_object, challange_string).
    The first can be passed to `checkchallenge` to check if answer is
    correct. The second can be passwed to `answerchallenge`.
    """
    pseed = ffi.new("char[]", seed)
    pchal = ffi.new("char **")
    chal = lib.genchallenge(pubkey, pseed, len(seed), pchal)
    gcchal = ffi.gc(chal, lib.freechallenge)
    return gcchal, _cstr2bs(pchal)


def checkchallenge(answerstr, answer):
    """ Second argument is a correct_answer_object returned by
    `genchallenge`.
    """
    panswer = ffi.new("char[]", answerstr)
    return bool(lib.checkchallenge(panswer, answer))


if __name__ == '__main__':
    """ Simple tests """

    # challenge
    priv, pub = genprivkey(b'hello world')
    pubkey = parsepubkey(pub)
    correct, chalstr = genchallenge(pubkey, b'hello there')
    ans = answerchallenge(priv, chalstr)
    assert checkchallenge(ans, correct), "failed: challange"

    # tiger hash
    expected = b'71414a27ee5ed703404021fbcc5530a2b01106f23fb7ee9e'
    actual = hashstring(b'abcdefghijklmnopqrstuvwxyz')
    assert actual == expected, "failed: tiger hash"
