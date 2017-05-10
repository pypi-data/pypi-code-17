class Helper:

    @staticmethod
    def to_hex(number):
        """
        Return the given number as an Ethereum compatible hex value
        :param number: Numeric value
        :return: Ethereum compatible hex representation of number, ex: 0x4f
        """
        return format(number, '#04x')

    @staticmethod
    def generate_empty_payload(method):
        """
        Generate a new empty payload with the supplied method and empty params
        :param method: JSON-RPC payload method
        :return:
        """
        return {
            "method": method,
            "params": [],
            "jsonrpc": "2.0",
        }

    @staticmethod
    def result_or_raw(raw, result):
        if raw:
            return result
        else:
            return result['result']


    @staticmethod
    def result_or_raw_quantity(raw, result):
        if raw:
            return result
        else:
            return int(result['result'], 16)
