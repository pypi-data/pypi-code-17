from .object import Object

class Group(Object):
    """
    Represents a Slack private channel or group.
    """
    def __init__(self, slack, group):
        Object.__init__(self, group)
        self._slack = slack

    async def write(self, text, **kwargs):
        """
        Writes a message to the group.

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
        Uploads a file to the group.

        Args:
            **kwargs: Arbitrary options to use when uploading
                the file. Refer to ``Slack#upload_file`` for more information.
                This is mostly a convenience method so you can directly
                upload files through a ``Group`` object.

        Returns:
            File: A ``File`` object representing the newly uploaded file.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.upload_file(self, **kwargs)

    async def get_history(self, **kwargs):
        """
        Fetches and returns the message history for the group.

        Args:
            **kwargs:
                Arbitrary options to use when fetching
                the group's message history. Refer to ``Slack#get_group_history``
                for more information. This is mostly a convenience method so
                you can directly fetch a group's message history.

        Returns:
            list (Message): A list of ``Message`` objects.
            bool: Whether or not there are more messages in the group's history.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.get_group_history(self, **kwargs)

    async def archive(self):
        """
        Archives the group.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.archive_group(self)

    async def unarchive(self):
        """
        Unarchives the group.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.unarchive_group(self)

    async def invite_user(self, user):
        """
        Invites a user to the group.
        
        Args:
            user (User): The user to invite to the group.
        
        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.archive_group(self, user)

    async def kick_user(self, user):
        """
        Kicks a user from the group.

        Args:
            user (User): The user to kick from the group.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.group_kick(self, user)

    async def leave(self):
        """
        Leaves the group.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.leave_group(self)

    async def mark(self, ts):
        """
        Changes the last-read indicator in the group
        for the current user.

        Args:
            ts (float): The timestamp to use when changing the
                last-read indicator.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.mark_group(self, ts)

    async def rename(self, name, validate=False):
        """
        Renames the group to something else.

        This method causes the current ``Group`` object to become stale.

        Args:
            name (str): The new name for the group.
            validate (bool): Whether or not to return an error instead
                of changing the new name to be valid. Defaults to ``False``.

        Returns:
            str: The new name for the group.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.rename_group(self, name, validate=validate)

    async def get_replies(self, ts):
        """
        Fetches and returns all replies to a message within the group.

        Args:
            ts: The timestamp of the parent message to look for.

        Returns:
            list (Message):
                A list of `Message` objects representing a message thread.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.get_group_replies(self, ts)

    async def set_purpose(self, purpose):
        """
        Sets the purpose for the group.

        This causes the ``Group`` object being worked on to become stale.

        Args:
            purpose: The purpose to use when updating the group.

        Returns:
            The new purpose of the group.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.set_group_purpose(self, purpose)

    async def set_topic(self, topic):
        """
        Sets the topic for the group.

        This causes the ``Group`` object being worked on to become stale.

        Args:
            topic: The topic to use when updating the group.

        Returns:
            The new topic of the group.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.set_group_topic(self, topic)

    async def close(self):
        """
        Closes the group.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.close_group(self)

    async def create_child(self):
        """
        Clones the group and then archives the original.

        Returns:
            Group:
                A ``Group`` object that is a clone of the original group.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        return await self._slack.create_group_child(self)

    async def open(self):
        """
        Opens the group channel.

        Raises:
            SlackError: Raised in the vent that Slack does not return ``ok``.
        """
        return await self._slack.open_group(self)

    async def list_members(self):
        """
        Fetches and returns a list of all group members.

        Returns:
            list (Member): All members in the group.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        all_users = await self._client.list_users()
        all_users = [User(x) for x in all_users]
        return [x for x in all_users if x.id in self.members] 

    async def update(self):
        """
        Updates the current ``Group`` object.
        There isn't much benefit to using this and it's here
        if you don't want to replace your current ``Group`` object
        or can't.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        updated_copy = self._slack.group_by_id(self.id)
        self.__dict__.update(updated_copy.__dict__)