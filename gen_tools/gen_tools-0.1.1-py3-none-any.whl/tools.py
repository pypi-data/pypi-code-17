import secrets
import string
import uuid


def gen_pass(pass_length: int = 8) -> str:
    """
    Return random alphanumeric str with a length of pass_length.

    :param pass_length: length of returned password.
    :return: generated password as str.
    """

    alphanumeric_chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphanumeric_chars)
                   for i in range(pass_length))


def gen_uuid(capitalize: bool = False) -> str:
    """
    Return random UUID. If capitalize is True then use upper case for letters.

    :param capitalize: whether or not to use upper case letters.
    :return: generated UUID as str.
    """

    if capitalize:
        resp = str(uuid.uuid4()).upper()
    else:
        resp = str(uuid.uuid4())

    return resp


def main():
    pass


if __name__ == '__main__':
    main()
