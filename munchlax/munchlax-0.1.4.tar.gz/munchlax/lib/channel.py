from .object import Object

class Channel(Object):
    """
    Represents a Slack channel.
    """
    def __init__(self, slack, channel):
        Object.__init__(self, channel)
        self._slack = slack

    async def write(self, text, **kwargs):
        """
        Writes a message to the channel.

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
        return await self._slack.raw_write(channel=self.id, text=text, **kwargs)

    async def upload(self, **kwargs):
        """
        Uploads a file to the channel.

        Args:
            **kwargs: Arbitrary options to use when uploading
                the file. Refer to ``Slack#upload_file`` for more information.
                This is mostly a convenience method so you can directly
                upload files through a ``Channel`` object.

        Returns:
            File: A ``File`` object representing the newly uploaded file.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.upload_file(self, **kwargs)

    async def get_history(self, **kwargs):
        """
        Fetches and returns the message history for the channel.

        Args:
            **kwargs: Arbitrary options to use when fetching
                the channel's message history. Refer to ``Slack#get_channel_history``
                for more information.
                This is mostly a convenience method so you can directly fetch
                a channel's message history.

        Returns:
            list (Message): A list of ``Message`` objects.
            bool: Whether or not there are more messages in the channel's history.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.get_channel_history(self, **kwargs)

    async def archive(self):
        """
        Archives the channel.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.archive_channel(self)

    async def unarchive(self):
        """
        Unarchives the channel.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.unarchive_channel(self)

    async def invite_user(self, user):
        """
        Invites a user to the channel.
        
        Args:
            user (User): The user to invite to the channel.
        
        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.archive_channel(self, user)

    async def join(self):
        """
        Joins the channel.

        In the event that the channel is already joined, then ``True``
        is returned instead of a ``Channel`` object for the joined
        channel.

        Args:
            channel (Channel): The channel to join. This channel
                must not be private.

        Returns:
            Channel or True: 
                If the user has not yet joined this channel
                then a ``Channel`` object representing the newly
                joined channel will be returned.

                If the channel to join has already been joined,
                then ``True`` will be returned instead.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.join_channel(self)

    async def kick_user(self, user):
        """
        Kicks a user from the channel.

        Args:
            user (User): The user to kick from the channel.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.channel_kick(self, user)

    async def leave(self):
        """
        Leaves the channel.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.leave_channel(self)

    async def mark(self, ts):
        """
        Changes the last-read indicator in the channel
        for the current user.

        Args:
            ts (float): The timestamp to use when changing the
                last-read indicator.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.mark_channel(self, ts)

    async def rename(self, name, validate=False):
        """
        Renames the channel to something else.

        This method causes the current ``Channel`` object to become stale.

        Args:
            name (str): The new name for the channel.
            validate (bool): Whether or not to return an error instead
                of changing the new name to be valid. Defaults to ``False``.

        Returns:
            str: The new name for the channel.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.rename_channel(self, name, validate=validate)

    async def get_replies(self, ts):
        """
        Fetches and returns all replies to a message within the channel.

        Args:
            ts: The timestamp of the parent message to look for.

        Returns:
            list (Message):
                A list of ``Message`` objects representing a message
                thread.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.get_channel_replies(self, ts)

    async def set_purpose(self, purpose):
        """
        Sets the purpose for the channel.

        This causes the ``Channel`` object being worked on to become stale.

        Args:
            purpose: The purpose to use when updating the channel.

        Returns:
            The new purpose of the channel.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.set_channel_purpose(self, purpose)

    async def set_topic(self, topic):
        """
        Sets the topic for the channel.

        This causes the ``Channel`` object being worked on to become stale.

        Args:
            topic: The topic to use when updating the channel.

        Returns:
            The new topic of the channel.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.set_channel_topic(self, topic)

    async def list_members(self):
        """
        Fetches and returns a list of all channel members.

        Returns:
            list (Member): All members in the channel.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        all_users = await self._client.list_users()
        all_users = [User(x) for x in all_users]
        return [x for x in all_users if x.id in self.members] 

    async def update(self):
        """
        Updates the current ``Channel`` object.

        There isn't much benefit to using this and it's here
        if you don't want to replace your current ``Channel`` object
        or can't.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        updated_copy = self._slack.channel_by_id(self.id)
        self.__dict__.update(updated_copy.__dict__)