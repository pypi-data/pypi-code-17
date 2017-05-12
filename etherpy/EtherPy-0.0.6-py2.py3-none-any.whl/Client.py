import requests, json, numbers
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
            Helper.to_hex(block)
        ]
        result = self.request(payload)
        return Helper.result_or_raw_quantity(raw, result)

    def eth_get_uncle_count_by_block_hash(self, block, raw=False):
        """
        Returns the number of uncles in a block from a block matching the given block hash
        :param block: hash of the block
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getUncleCountByBlockHash")
        payload['params'] = [
            block
        ]
        result = self.request(payload)
        return Helper.result_or_raw_quantity(raw, result)

    def eth_get_uncle_count_by_block_number(self, block, raw=False):
        """
        Returns the number of uncles in a block from a block matching the given block number
        :param block: number of the block
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getUncleCountByBlockNumber")
        payload['params'] = [
            Helper.to_hex(block)
        ]
        result = self.request(payload)
        return Helper.result_or_raw_quantity(raw, result)

    def eth_get_code(self, address, block_number="latest", raw=False):
        """
        Returns code at the given address
        :param address: Ethereum address
        :param block_number:  integer block number, or the string "latest", "earliest" or "pending"
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getCode")
        payload['params'] = [
            address,
            block_number
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_sign(self, address, message_to_sign, raw=False):
        """
        The sign method calculates an Ethereum specific signature with:
        sign(keccak256("\x19Ethereum Signed Message:\n" + len(message) + message))).

        By adding a prefix to the message makes the calculated signature recognisable
        as an Ethereum specific signature. This prevents misuse where a malicious DApp can sign arbitrary data
        (e.g. transaction) and use the signature to impersonate the victim.

        Note the address to sign with must be unlocked.

        Example https://gist.github.com/bas-vk/d46d83da2b2b4721efb0907aecdb7ebd
        :param address: Ethereum address
        :param message_to_sign:  N-Bytes message to sign
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getCode")
        payload['params'] = [
            address,
            message_to_sign
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_send_transaction(self, from_address, data, to_address=None,
                             gas=None, gas_price=None, value=None, nonce=None, raw=False):
        """
        Creates new message call transaction or a contract creation, if the data field contains code.

        :param from_address: The address to send from
        :param to_address: (optional when creating new contract) The address the transaction is directed to
        :param gas: (optional, default: 90000) Integer of the gas provided for the transaction execution. It will return
        unused gas.
        :param gas_price: (optional, default: To-Be-Determined) Integer of the gasPrice used for each paid gas
        :param value: (optional) Integer value to send with the transaction
        :param data: The compiled code of a contract OR the hash of the invoked method signature and encoded parameters.
         For details see: https://github.com/ethereum/wiki/wiki/Ethereum-Contract-ABI
        :param nonce: (optional) Integer of a nonce. This allows to overwrite your own pending transactions that use the
        same nonce
        :param raw:
        :return: The transaction hash, or the zero hash if the transaction is not yet available.

        Use eth_getTransactionReceipt to get the contract address, after the transaction was mined,
        when you created a contract.
        """
        payload = Helper.generate_empty_payload("eth_sendTransaction")
        transaction_object = {
            "from": from_address
        }
        if to_address:
            transaction_object['to'] = to_address
        if gas:
            transaction_object['gas'] = gas
        if gas_price:
            transaction_object['gasPrice'] = gas_price
        if value:
            transaction_object['value'] = value
        if data:
            transaction_object['data'] = data
        if nonce:
            transaction_object['nonce'] = nonce
        payload['params'] = [
            transaction_object
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_send_raw_transaction(self, data, raw=False):
        """
        Creates new message call transaction or a contract creation for signed transactions.
        :param data: signed transaction data
        :param raw:
        :return: The transaction hash, or the zero hash if the transaction is not yet available.

        Use eth_getTransactionReceipt to get the contract address, after the transaction was mined,
        when you created a contract.
        """
        payload = Helper.generate_empty_payload("eth_sendRawTransaction")
        payload['params'] = [
            data
        ]

        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_call(self, from_address, data, to_address=None,
                             gas=None, gas_price=None, value=None, block="latest", raw=False):
        """
        Executes a new message call immediately without creating a transaction on the block chain.

        :param from_address: (optional) The address the transaction is sent from.
        :param to_address: The address the transaction is directed to.
        :param gas: (optional) Integer of the gas provided for the transaction execution. eth_call consumes zero gas,
        but this parameter may be needed by some executions.
        :param gas_price: (optional, default: To-Be-Determined) Integer of the gasPrice used for each paid gas
        :param value: (optional) Integer value to send with the transaction
        :param data: (optional) Hash of the method signature and encoded parameters. For details see:
        https://github.com/ethereum/wiki/wiki/Ethereum-Contract-ABI
        :param block:  integer block number, or the string "latest", "earliest" or "pending"
        :param raw:
        :return: The return value of executed contract
        """
        payload = Helper.generate_empty_payload("eth_call")
        transaction_object = {
            "to": to_address
        }
        if from_address:
            transaction_object['from'] = to_address
        if gas:
            transaction_object['gas'] = gas
        if gas_price:
            transaction_object['gasPrice'] = gas_price
        if value:
            transaction_object['value'] = value
        if data:
            transaction_object['data'] = data
        payload['params'] = [
            transaction_object,
            block
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_estimate_gas(self, from_address, data, to_address=None,
                             gas=None, gas_price=None, value=None, nonce=None, raw=False):
        """
        Makes a call or transaction, which won't be added to the blockchain and returns the used gas,
        which can be used for estimating the used gas.

        Parameters

        See eth_call parameters, expect that all properties are optional.
        If no gas limit is specified geth uses the block gas limit from the pending block as an upper bound.
        As a result the returned estimate might not be enough to executed the call/transaction when the amount of gas
        is higher than the pending block gas limit.

        :param from_address: (optional) The address to send from
        :param to_address: (optional when creating new contract) The address the transaction is directed to
        :param gas: (optional, default: 90000) Integer of the gas provided for the transaction execution. It will return
        unused gas.
        :param gas_price: (optional, default: To-Be-Determined) Integer of the gasPrice used for each paid gas
        :param value: (optional) Integer value to send with the transaction
        :param data: The compiled code of a contract OR the hash of the invoked method signature and encoded parameters.
         For details see: https://github.com/ethereum/wiki/wiki/Ethereum-Contract-ABI
        :param nonce: (optional) Integer of a nonce. This allows to overwrite your own pending transactions that use the
        same nonce
        :param raw:
        :return: The amount of gas used.
        """
        payload = Helper.generate_empty_payload("eth_sendTransaction")
        transaction_object = {
        }
        if from_address:
            transaction_object['from'] = from_address
        if to_address:
            transaction_object['to'] = to_address
        if gas:
            transaction_object['gas'] = gas
        if gas_price:
            transaction_object['gasPrice'] = gas_price
        if value:
            transaction_object['value'] = value
        if data:
            transaction_object['data'] = data
        if nonce:
            transaction_object['nonce'] = nonce
        payload['params'] = [
            transaction_object
        ]
        result = self.request(payload)
        return Helper.result_or_raw_quantity(raw, result)

    def eth_get_block_by_hash(self, block, transactions=False, raw=False):
        """
        Get information about a block based on its hash
        :param block: hash of the block
        :param transactions: if true it returns the full transaction objects,
        if false only the hashes of the transactions
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getBlockByHash")
        payload['params'] = [
            block,
            transactions
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_get_block_by_number(self, block="latest", transactions=False, raw=False):
        """
        Get information about a block based on its number
        :param block: integer of a block number, or the string "earliest", "latest" or "pending"
        :param transactions: if true it returns the full transaction objects,
        if false only the hashes of the transactions
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getBlockByNumber")
        payload['params'] = [
            Helper.to_hex(block) if isinstance(block, numbers.Number) else block,
            transactions
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_get_transaction_by_hash(self, transaction, raw=False):
        """
        Returns the information about a transaction requested by transaction hash.
        :param transaction: hash of the transaction
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getTransactionByHash")
        payload['params'] = [
            transaction
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_get_transaction_by_block_hash_and_index(self, transaction, index, raw=False):
        """
        Returns the information about a transaction requested by transaction hash.
        :param transaction: hash of the transaction
        :param index: Integer of the transaction index position
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getTransactionByBlockHashAndIndex")
        payload['params'] = [
            transaction,
            Helper.to_hex(index)
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_get_transaction_by_block_number_and_index(self, block="latest", index=0, raw=False):
        """
        Returns the information about a transaction requested by transaction hash.
        :param block: a block number, or the string "earliest", "latest" or "pending
        :param index: Integer of the transaction index position
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getTransactionByBlockNumberAndIndex")
        payload['params'] = [
            Helper.to_hex(block) if isinstance(block, numbers.Number) else block,
            Helper.to_hex(index)
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_get_transaction_receipt(self, transaction, raw=False):
        """
        Returns the receipt of a transaction by transaction hash.

        Note That the receipt is not available for pending transactions.
        :param transaction: hash of a transaction
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getTransactionReceipt")
        payload['params'] = [
            transaction
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_get_uncle_by_block_hash_and_index(self, block, index, raw=False):
        """
        Returns information about a uncle of a block by hash and uncle index position.
        :param block: hash of a block
        :param index: the uncle's index position
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getUncleByBlockHashAndIndex")
        payload['params'] = [
            block,
            Helper.to_hex(index)
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_get_uncle_by_block_number_and_index(self, block="latest", index=0, raw=False):
        """
        Returns information about a uncle of a block by number and uncle index position.
        :param block: a block number, or the string "earliest", "latest" or "pending"
        :param index: the uncle's index position
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getUncleByBlockNumberAndIndex")
        payload['params'] = [
            Helper.to_hex(block) if isinstance(block, numbers.Number) else block,
            Helper.to_hex(index)
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_get_compilers(self, raw=False):
        """
        Returns a list of available compilers in the client.
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getCompilers")
        payload['params'] = []
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_compile_solidity(self, source, raw=False):
        """
        Returns compiled solidity code.
        :param source: The source code
        :param raw:
        :return: The compiled source code
        """
        payload = Helper.generate_empty_payload("eth_compileSolidity")
        payload['params'] = [
            source
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_compile_lll(self, source, raw=False):
        """
        Returns compiled LLL code.
        :param source: The source code
        :param raw:
        :return: The compiled source code
        """
        payload = Helper.generate_empty_payload("eth_compileLLL")
        payload['params'] = [
            source
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_compile_serpent(self, source, raw=False):
        """
        Returns compiled serpent code.
        :param source: The source code
        :param raw:
        :return:The compiled source code
        """
        payload = Helper.generate_empty_payload("eth_compileSerpent")
        payload['params'] = [
            source
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_new_filter(self):
        """
        TODO This
        :return:
        """
        raise NotImplemented

    def eth_new_block_filter(self):
        """
        TODO This
        :return:
        """
        raise NotImplemented

    def eth_new_pending_transaction_filter(self):
        """
        TODO This
        :return:
        """
        raise NotImplemented

    def eth_uninstall_filter(self):
        """
        TODO This
        :return:
        """
        raise NotImplemented

    def eth_get_filter_changes(self):
        """
        TODO This
        :return:
        """
        raise NotImplemented

    def eth_get_filter_logs(self):
        """
        TODO This
        :return:
        """
        raise NotImplemented

    def eth_get_logs(self):
        """
        TODO this
        :return:
        """
        raise NotImplemented

    def eth_get_work(self, raw=False):
        """
        Returns the hash of the current block, the seedHash, and the boundary condition to be met ("target").
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_getWork")
        payload['params'] = []

        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_submit_work(self, nonce, pow_hash, mix, raw=False):
        """
        Used for submitting a proof-of-work solution
        :param nonce: The nonce found (64 bits)
        :param pow_hash: The header's pow-hash (256 bits)
        :param mix: The mix digest (256 bits)
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_submitWork")
        payload['params'] = [
            nonce,
            pow_hash,
            mix
        ]

        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def eth_submit_hashrate(self, hashrate, id_hash, raw=False):
        """
        Used for submitting mining hashrate
        :param hashrate: A hex string representation 32 bytes of the hash rate
        :param id_hash: A random hexadecimal (32 bytes) ID identifying the client
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("eth_submitHashrate")
        payload['params'] = [
            Helper.to_hex(hashrate),
            Helper.to_hex(id_hash)
        ]

        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def db_put_string(self, db_name, key, value, raw=False):
        """
        Stores a string in the local database.

        Note this function is deprecated and will be removed in the future.
        :param db_name: Database name
        :param key: Key name
        :param value: String to store
        :param raw:
        :return: returns true if the value was stored, otherwise false.
        """
        payload = Helper.generate_empty_payload("db_putString")
        payload['params'] = [
            db_name,
            key,
            value
        ]

        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def db_get_string(self, db_name, key, raw=False):
        """
        Returns string from the local database.

        Note this function is deprecated and will be removed in the future.
        :param db_name: Database name
        :param key: Key name
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("db_getString")
        payload['params'] = [
            db_name,
            key
        ]

        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def db_put_hex(self, db_name, key, value, raw=False):
        """
        Stores binary data in the local database.

        Note this function is deprecated and will be removed in the future.
        :param db_name: Database name
        :param key: Key name
        :param value: String to store
        :param raw:
        :return: returns true if the value was stored, otherwise false.
        """
        payload = Helper.generate_empty_payload("db_putHex")
        payload['params'] = [
            db_name,
            key,
            Helper.to_hex(value) if isinstance(value, numbers.Number) else value
        ]

        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def db_get_hex(self, db_name, key, raw=False):
        """
        Returns binary data from the local database.

        Note this function is deprecated and will be removed in the future.
        :param db_name: Database name
        :param key: Key name
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("db_getHex")
        payload['params'] = [
            db_name,
            key
        ]

        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def ssh_version(self, raw=False):
        """
        Returns the current whisper protocol version
        :param raw:
        :return:
        """

        payload = Helper.generate_empty_payload("ssh_version")
        payload['params'] = []

        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def ssh_post(self, topics, payload, priority, ttl, from_address=None, to_address=None, raw=False):
        """
        Sends a whisper message
        :param topics: Array of DATA - Array of DATA topics, for the receiver to identify messages.
        :param payload: The payload of the message.
        :param priority: The integer of the priority in a rang from ... (?).
        :param ttl: integer of the time to live in seconds.
        :param from_address: (optional) The identity of the sender.
        :param to_address: (optional) The identity of the receiver. When present whisper will encrypt the message
        so that only the receiver can decrypt it.
        :param raw:
        :return: returns true if the message was send, otherwise false.
        """

        payload = Helper.generate_empty_payload("ssh_post")
        payload['params'] = []

        ssh_obj = {
            "topics": [],
            "payload": Helper.to_hex(payload) if isinstance(payload, numbers.Number) else payload,
            "priority": Helper.to_hex(priority),
            "ttl": Helper.to_hex(ttl)
        }
        for topic in topics:
            ssh_obj['topic'].append(
                Helper.to_hex(topic) if isinstance(topic, numbers.Number) else topic
            )

        if from_address:
            ssh_obj['from'] = from_address
        if to_address:
            ssh_obj['to'] = to_address

        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def ssh_new_identity(self, raw=False):
        """
        Creates new whisper identity in the client.
        :param raw:
        :return: the address of the new identity.
        """

        payload = Helper.generate_empty_payload("ssh_newIdentity")
        payload['params'] = []

        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def ssh_has_identity(self, address, raw=False):
        """
        Checks if the client hold the private keys for a given identity.
        :param address: The identity address to check
        :param raw:
        :return: returns true if the client holds the privatekey for that identity, otherwise false.
        """

        payload = Helper.generate_empty_payload("ssh_hasIdentity")
        payload['params'] = [
            address
        ]

        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

    def ssh_new_group(self):
        """
        TODO Implement this if it's actually a real thing
        :return:
        """
        raise NotImplemented

    def ssh_add_to_group(self):
        """
        TODO Implement this if it's actually a real thing
        :return:
        """
        raise NotImplemented

    def ssh_new_filter(self):
        """
        TODO Implement
        :return:
        """
        raise NotImplemented

    def ssh_uninstall_filter(self):
        """
        TODO Implement
        :return:
        """
        raise NotImplemented

    def ssh_get_filter_changes(self):
        """
        TODO Implement
        :return:
        """
        raise NotImplemented

    def ssh_get_messages(self, filter, raw=False):
        """
        Get all messages matching a filter. Unlike ssh_get_filter_changes this returns all message
        :param filter: Filter id
        :param raw:
        :return:
        """
        payload = Helper.generate_empty_payload("ssh_getMessages")
        payload['params'] = [
            Helper.to_hex(filter) if isinstance(filter, numbers.Number) else filter,
        ]
        result = self.request(payload)
        return Helper.result_or_raw(raw, result)

