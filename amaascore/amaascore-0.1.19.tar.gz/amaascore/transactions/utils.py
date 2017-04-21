from __future__ import absolute_import, division, print_function, unicode_literals

from amaascore.transactions.position import Position
from amaascore.transactions.transaction import Transaction


def json_to_position(json_position):
    position = Position(**json_position)
    return position


def json_to_transaction(json_transaction):
    for (collection_name, clazz) in Transaction.children().items():
        children = json_transaction.pop(collection_name, {})
        collection = {}
        for (child_type, child_json) in children.items():
            # Handle the case where there are multiple children for a given type - e.g. links
            if isinstance(child_json, list):
                child = set()
                for child_json_in_list in child_json:
                    child.add(clazz(**child_json_in_list))
            else:
                child = clazz(**child_json)
            collection[child_type] = child
        json_transaction[collection_name] = collection
    transaction = Transaction(**json_transaction)
    return transaction

