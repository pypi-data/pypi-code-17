from rpc.client import VisaRpcClient
from core import common

defaultMessageQueueConfiguration = {
    'mq': {
        # 'host': 'box.cherubits.hu',
        'host': 'localhost',
        'port': 5672,
        # 'username': 'hedgehog',
        'username': 'guest',
        # 'password': 'qwe123',
        'password': 'guest',
        'exchange': 'visa_rpc'
    }
}
externalizedMessageQueueConfiguration = common.loadConfiguration("/opt/hedgehog-station-controller/mq.yml",
                                                                 defaults=defaultMessageQueueConfiguration)
client = VisaRpcClient(
    exchange=externalizedMessageQueueConfiguration['mq']['exchange'],
    host=externalizedMessageQueueConfiguration['mq']['host'],
    port=externalizedMessageQueueConfiguration['mq']['port'],
    username=externalizedMessageQueueConfiguration['mq']['username'],
    password=externalizedMessageQueueConfiguration['mq']['password']
)
