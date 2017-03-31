from kik.messages.message import Message


class FriendPickerMessage(Message):
    """
    A friend picker message, as documented at `<https://dev.kik.com/#/docs/messaging#friend-picker-response-object>`_.
    """
    def __init__(self, picked=None, chat_type=None, **kwargs):
        super(FriendPickerMessage, self).__init__(type='friend-picker', **kwargs)
        self.picked = picked
        self.chat_type = chat_type

    @classmethod
    def property_mapping(cls):
        mapping = super(FriendPickerMessage, cls).property_mapping()
        mapping.update({
            'picked': 'picked',
            'chat_type': 'chatType'
        })
        return mapping
