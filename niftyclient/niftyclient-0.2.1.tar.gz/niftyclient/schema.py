from dictobj import DictionaryObject, MutableDictionaryObject
from marshmallow import Schema, fields, post_load


class ResponseSchema(Schema):
    limit = fields.Int()
    offset = fields.Int()
    available_resultset_size = fields.Int()
    returned_resultset_size = fields.Int()
    tracking_uuid = fields.UUID()


class WalletSchema(ResponseSchema):
    class Wallet(Schema):
        user_name = fields.Str()
        user_id = fields.UUID()
        created_at = fields.DateTime()
        last_modified = fields.DateTime()
        balance = fields.Decimal()
    returned_resultset = fields.Nested(Wallet, many=True)

    @post_load
    def make_wallet(self, data):
        returned_resultset = data.pop('returned_resultset', [])
        result = MutableDictionaryObject(data)
        result.wallets = [DictionaryObject(resultset) for resultset in returned_resultset]
        return result

class TransactionSchema(ResponseSchema):
    class Transaction(Schema):
        msisdn = fields.Str()
        names = fields.Str()
        till_number = fields.Str()
        trans_id = fields.Str()
        payment_id = fields.UUID()
        user_id = fields.UUID()
        trans_time = fields.DateTime()
        trans_amount = fields.Decimal()
    returned_resultset = fields.Nested(Transaction, many=True)

    @post_load
    def make_transaction(self, data):
        returned_resultset = data.pop('returned_resultset', [])
        result = MutableDictionaryObject(data)
        result.transactions = [DictionaryObject(resultset) for resultset in returned_resultset]
        return result
