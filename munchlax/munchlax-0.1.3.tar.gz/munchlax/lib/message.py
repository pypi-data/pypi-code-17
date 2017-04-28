from .object import Object

class Message(Object):
    """
    Represents a Slack channel.
    """
    def __init__(self, slack, message):
        Object.__init__(self, message)
        self._slack = slack

    async def reply(self, text, **kwargs):
        """
        Writes a reply to the message.

        This is basically a convenience function for:
        
        ``slack.raw_write(text=text, channel=message.channel)``

        Args:
            text (str): The text of the message.
            **kwargs: Additional options to use when sending the
                message. Refer to ``Slack#raw_write`` for more information.
                In most cases, you will only need to specify ``text`` if you
                only want to send a text message.
            
        Returns:
            Message: A ``Message`` object representing the newly sent message.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.raw_write(text=text, channel=self.channel, **kwargs)

    async def delete(self):
        """
        Deletes the message.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.delete(self)

    async def edit(self, text, **kwargs):
        """
        Updates the message's contents.

        Args:
            text (str): The new message contents. 
            **kwargs: Additional options to use when updating the message.
                Refer to ``Slack#raw_edit`` for more information.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        msg = await self._slack.edit(self, text=text, **kwargs)
        self.__dict__.update(msg.__dict__)
        return self

    async def get_author(self):
        """
        Returns the author of the message as either a ``User`` or ``Bot`` object.

        Returns:
            User or Bot or None:
                The author of the message.

                In the event that a message has no author, ``None`` will be returned.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        if getattr(self, 'user', None) is not None:
            return await self._slack.user_by_id(self.user)
        elif getattr(self, 'bot', None) is not None:
            return await self._slack.bot_by_id(self.bot)
        else:
            return None

    async def get_channel(self):
        """
        Returns the channel that contains the message.

        Returns:
            Channel: The channel that contains the message.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.channel_by_id(self.id)

    async def get_replies(self):
        """
        Fetches all replies to a message and returns them.

        Returns:
            list (Message):
                A list of ``Message`` objects representing a message thread.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        channel = await self.get_channel()
        return await self._slack.get_channel_replies(channel, self.ts)