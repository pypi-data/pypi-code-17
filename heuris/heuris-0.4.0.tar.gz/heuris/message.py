from enum import IntEnum
import json

class MessageOpcode(IntEnum):
    ERROR = 0
    SUCCESS = 1
    MEASUREMENT = 2
    LOGIN = 3

class Message:
    def __init__(self, opcode = MessageOpcode.ERROR):
        self.opcode = opcode
        self.entries = {}
    
    def __eq__(self, other):
        return self.opcode == other.opcode and self.entries == other.entries

class MessageSerializer:
    @staticmethod
    def serialize(msg):
        data = {}

        data['opcode'] = int(msg.opcode)
        if len(msg.entries) > 0:
            data['entries'] = msg.entries

        return json.dumps(data).encode()

class MessageDeserializer:
    @staticmethod
    def deserialize(payload):
        obj = json.loads(payload.decode())
        msg = Message(MessageOpcode(obj['opcode']))
        if 'entries' in obj:
            msg.entries = obj['entries']
        return msg
