import sys
import uuid


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


def main(caps=False):
    sys.stdout.write(gen_uuid(capitalize=caps))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
