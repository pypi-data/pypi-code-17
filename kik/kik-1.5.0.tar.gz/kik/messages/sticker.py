from kik.messages.message import Message


class StickerMessage(Message):
    """
    A full sticker message object, as documented at `<https://dev.kik.com/#/docs/messaging#sticker>`_.
    """
    def __init__(self, sticker_pack_id=None, sticker_url=None, chat_type=None, **kwargs):
        super(StickerMessage, self).__init__(type='sticker', **kwargs)
        self.sticker_pack_id = sticker_pack_id
        self.sticker_url = sticker_url
        self.chat_type = chat_type

    @classmethod
    def property_mapping(cls):
        mapping = super(StickerMessage, cls).property_mapping()
        mapping.update({
            'sticker_pack_id': 'stickerPackId',
            'sticker_url': 'stickerUrl',
            'chat_type': 'chatType'
        })
        return mapping
