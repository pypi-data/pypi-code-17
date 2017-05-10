import requests
import json
from .Helper import Helper


class Client:

    requestCount = 0

    def __init__(self, host, port):
        """
        Instantiate a new Ethereum Node client with the supplied host and port.
        :param host: Host/IPAddress to connect to
        :param port: Port to connect to JSON-RPC
        """
        self.host = host
        self.port = port
        print("{0} {1}".format(host, port))

    def request(self, payload):
        self.requestCount += 1
        url = "http://{0}:{1}".format(self.host, self.port)
        headers = {'content-type': 'application/json'}

        payload['id'] = self.requestCount
        response = requests.post(
            url, data=json.dumps(payload), headers=headers).json()

        return response

    def web3_client_version(self, raw=False):
        """
        Get web3 client Version
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("web3_clientVersion")
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def web3_sha3(self, data, raw=False):
        """
        Compute the Keccak-256 of the given data
        :param data:
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("web3_sha3")
        payload['params'] = [
            data
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def net_version(self, raw=False):
        """
        Get the current network version for the node
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("net_version")
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def net_listening(self, raw=False):
        """
        Get if the node is listening for new connections
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("net_listening")
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def net_peer_count(self, raw=False):
        """
        Get the current peer count for the node
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("net_peerCount")
        result = self.request(payload)
        if raw:
            return result
        else:
            return int(result['result'], 16)

    def eth_protocol_version(self, raw=False):
        """
        Get the node's protocol version
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_protocolVersion")
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_syncing(self, raw=False):
        """
        Get if the node is syncing
        :param raw:
        :return: Returns false if not syncing, object if syncing
        """
        payload = Helper.generate_empty_payload("eth_syncing")
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_coinbase(self, raw=False):
        """
        Get the node's coinbase
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_coinbase")
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_mining(self, raw=False):
        """
        Get if the node is mining
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_mining")
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_hashrate(self, raw=False):
        """
        Get the hashrate of the node in hashes per second
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_hashrate")
        result = self.request(payload)
        return Helper.result_or_raw_quantity(raw, result)

    def eth_gas_price(self, raw=False):
        """
        Get the network gas price
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_gasPrice")
        result = self.request(payload)
        return Helper.result_or_raw_quantity(raw, result)

    def eth_accounts(self, raw=False):
        """
        Get accounts owned by the client
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_accounts")
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_block_number(self, raw=False):
        """
        Get the current block number
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_blockNumber")
        result = self.request(payload)
        return Helper.result_or_raw_quantity(raw, result)

    def eth_get_balance(self, address, block_number="latest", raw=False):
        """
        Get the balance of the given address in wei
        :param address: address to get balance of
        :param block_number: integer block number, or the string "latest", "earliest" or "pending"
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getBalance")
        payload['params'] = [
            address,
            block_number
        ]
        result = self.request(payload)
        return Helper.result_or_raw_quantity(raw, result)

    def eth_get_storage_at(self, address, position, block_number="latest", raw=False):
        """
        Returns the value from a storage position at a given address.
        :param address: Address of the storage
        :param position: integer of the position in the storage in Ethereum compatible hex string
        :param block_number: integer block number, or the string "latest", "earliest" or "pending"
        :param raw:
        :return:
        """
        #TODO:Support Hashmap
        payload = Helper.generate_empty_payload("eth_getStorageAt")
        payload['params'] = [
            address,
            position,
            block_number
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_get_transaction_count(self, address, block_number="latest", raw=False):
        """
        Get the number of transactions **sent** from an address
        :param address: address to get balance of
        :param block_number: integer block number, or the string "latest", "earliest" or "pending"
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getTransactionCount")
        payload['params'] = [
            address,
            block_number
        ]
        result = self.request(payload)
        return Helper.result_or_raw_quantity(raw, result)

    def eth_get_block_transaction_count_by_hash(self, block, raw=False):
        """
        Get the number of transactions in a block
        :param block: hash of the block
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getBlockTransactionCountByHash")
        payload['params'] = [
            block
        ]
        result = self.request(payload)
        return Helper.result_or_raw_quantity(raw, result)

    def eth_get_block_transaction_count_by_number(self, block, raw=False):
        """
        Get the number of transactions in a block
        :param block: block number
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getBlockTransactionCountByNumber")
        payload['params'] = [
            block
        ]
        result = self.request(payload)
        return Helper.result_or_raw_quantity(raw, result)

