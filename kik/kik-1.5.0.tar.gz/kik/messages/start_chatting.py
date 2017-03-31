from kik.messages.message import Message


class StartChattingMessage(Message):
    """
    A full start-chatting message object, as documented at `<https://dev.kik.com/#/docs/messaging#start-chatting>`_.
    """
    def __init__(self, chat_type=None, **kwargs):
        super(StartChattingMessage, self).__init__(type='start-chatting', **kwargs)
        self.chat_type = chat_type

    @classmethod
    def property_mapping(cls):
        mapping = super(StartChattingMessage, cls).property_mapping()
        mapping.update({
            'chat_type': 'chatType'
        })
        return mapping
