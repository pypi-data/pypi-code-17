from pynms.nms_client import NmsClient

__version__ = '0.1.0'


def connect(ak, sk, endpoint, queue_name):
    return NmsClient(ak, sk, endpoint, queue_name)
