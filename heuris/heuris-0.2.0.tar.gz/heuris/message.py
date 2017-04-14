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

    def serialize(self):
        data = {}

        data['opcode'] = self.opcode
        if len(self.entries) > 0:
            data['entries'] = self.entries

        return json.dumps(data).encode()
    
    def deserialize(payload):
        obj = json.loads(payload.decode())
        msg = Message(MessageOpcode(obj['opcode']))
        if 'entries' in obj:
            msg.entries = obj['entries']
        return msg
