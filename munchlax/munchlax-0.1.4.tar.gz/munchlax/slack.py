import asyncio
from datetime import datetime, timedelta
import json
from slackclient import SlackClient

from .slackerror import SlackError

from .lib.async import async_wrapper
from .lib.object import Object
from .lib.channel import Channel
from .lib.comment import Comment
from .lib.group import Group
from .lib.im import IM
from .lib.message import Message
from .lib.mpim import MPIM
from .lib.user import User

class Slack(object):
    def __init__(self):
        self._listeners = {}
        self._transforms = {}
        self._loop = None
        self._client = None

        self.transform('message', self._transform_message)

    ########################################
    # BUILT-IN TRANSFORMATIONS
    ########################################

    async def _transform_message(self, message):
        return Message(self, message)

    ########################################
    # SLACK METHODS
    ########################################

    async def channel_by_id(self, id):
        """
        Fetches a Slack channel by its ID and returns a ``Channel`` object.

        Args:
            id (str): The ID of the channel to get information for.

        Returns:
            Channel: A ``Channel`` object representing the channel requested.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        channel = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.info',
            channel=id
        )

        if channel['ok']:
            return Channel(self, channel['channel'])

        raise SlackError(channel['error'])

    async def group_by_id(self, id):
        """
        Fetches a Slack group by its ID and returns a ``Group`` object.

        Args:
            id (str): The ID of the group to get information for.

        Returns:
            Group: A ``Group`` object representing the group requested.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        group = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.info',
            channel=id
        )

        if group['ok']:
            return Group(self, group['group'])

        raise SlackError(channel['error'])

    async def user_by_id(self, uid):
        """
        Fetches a Slack use by their ID and returns a ``User`` object.

        Args:
            id (str): The ID of the user to get information for.

        Returns:
            User: A ``User`` object representing the user requested.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        user = await async_wrapper(
            self._loop,
            self._client.api_call,
            'users.info',
            user=uid
        )

        if user['ok']:
            return User(self, user['user'])
        
        raise SlackError(user['error'])

    async def bot_by_id(self, bid):
        """
        Fetches a Slack bot by its ID and returns a ``Bot`` object.

        Args:
            id (str): The ID of the bot to get information for.

        Returns:
            Bot: A ``Bot`` object representing the bot requested.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        bot = await async_wrapper(
            self._loop,
            self._client.api_call,
            'bot.info',
            bot=bid
        )

        if bot['ok']:
            return User(self, bot['bot'])
        
        raise SlackError(bot['error'])

    async def file_by_id(self, fid):
        """
        Fetches a file by its ID and returns a ``File`` object.

        Args:
            id (str): The ID of the file to get information for.

        Returns:
            File: A ``File`` object representing the File requested.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        f = await async_wrapper(
            self._loop,
            self._client.api_call,
            'files.info',
            file=fid
        )

        if f['ok']:
            return File(self, f['file'])
        
        raise SlackError(f['error'])

    async def create_channel(self, name, validate=False):
        """
        Creates a Slack channel. If the Slack channel already
        exists this method will still succeed.

        Args:
            name (str): The name of the new channel.
            validate (bool): Whether or not Slack should return an error
                if `name` is invalid instead of modifying it to be valid.
                For more information, refer to 
                https://api.slack.com/methods/channels.create.

        Returns:
            Channel: A ``Channel`` object representing the newly created channel.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        channel = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.create',
            name=name,
            validate=validate
        )

        if channel['ok']:
            return Channel(self, channel['channel'])
        
        raise SlackError(channel['error'])

    async def create_group(self, name, validate=False):
        """
        Creates a Slack group channel. If the group channel already
        exists this method will still succeed.

        Args:
            name (str): The name of the new group channel.
            validate (bool): Whether or not Slack should return an error
                if `name` is invalid instead of modifying it to be valid.
                For more information, refer to 
                https://api.slack.com/methods/channels.create.
                Defaults to False.

        Returns:
            Group: A ``Group`` object representing the newly created group.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        group = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.create',
            name=name,
            validate=validate
        )

        if group['ok']:
            return Group(self, group['group'])

        raise SlackError(group['error'])

    async def list_channels(self, exclude_archived=False):
        """
        Fetches and returns all channels that are not private.
        To list all private channels use `Slack#list_groups`.

        Args:
            exclude_archived (bool): Whether or not to exclude
                archived channels from the list.
                Defaults to False.

        Returns:
            list (Channel): A list of ``Channel`` objects.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        channels = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.list',
            exclude_archived=exclude_archived
        )

        if channels['ok']:
            return [Channel(self, x) for x in channels['channels']]

        raise SlackError(channels['error'])

    async def list_groups(self, exclude_archived=False):
        """
        Fetchs and returns all private channels that the current
        user has access to.

        Args:
            exclude_archived (bool): Whether or not to exclude
                archived channels from the list.
                Defaults to False.

        Returns:
            list (Group): A list of ``Group`` objects.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        groups = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.list',
            exclude_archived=exclude_archived
        )

        if groups['ok']:
            return [Group(self, x) for x in groups['groups']]

        raise SlackError(groups['error'])

    async def list_ims(self):
        """
        Fetches and returns all IM channels that a user has.

        Returns:
            list (IM): A list of ``IM`` objects.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        ims = await async_wrapper(
            self._loop,
            self._client.api_call,
            'im.list'
        )

        if ims['ok']:
            return [IM(self, x) for x in ims['ims']]

        raise SlackError(ims['error'])

    async def list_mpims(self):
        """
        Fetches and returns all MPIM channels that a user has.

        Returns:
            list (MPIM): A list of ``MPIM`` objects.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        groups = await async_wrapper(
            self._loop,
            self._client.api_call,
            'mpim.list',
        )

        if groups['ok']:
            return [Group(self, x) for x in groups['groups']]

        raise SlackError(groups['error'])

    async def list_users(self, presence=True):
        """
        Fetches and returns all users in a team. This list will
        include deleted and eactivated users.

        Args:
            presence (bool): Whether or not to include presence
                data when returning the list of users.
                Defaults to True.

        Returns:
            list (User): A list of ``User`` objects representing all
                users in a team.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        users = await async_wrapper(
            self._loop,
            self._client.api_call,
            'users.list',
            presence=presence
        )
        
        if users['ok']:
            return [User(self, x) for x in users['members']]
        
        raise SlackError(users['error'])

    async def list_files(self, user=None, channel=None, ts_from=0, ts_to='now', types='all', count=100, page=1):
        """
        Fetches and returns all files uploaded in a team.

        Args:
            user (User): If this is passed then only files uploaded by ``User``
                will be returned.
            channel (Channel): If this is passed then only files shared
                to this channel will be returned.
            ts_from (float): All filters before this timestamp will be filtered out.
                Defaults to 0.
            ts_to (float | ``now``): All filters after this timestamp will be filtered out.
                It should be noted that ``now`` can be specified to fetch all files
                up to the current time.
                Defaults to ``now``.
            types (string): Specific filetypes to filter by. This should be
                a comma-delimited string. Alternatively, you can pass "all"
                to not filter by filetype.
                For more information, refer to https://api.slack.com/types/file.
                Defaults to "all".
            count (int): The number of files to return per page.
            page (int): The page number to show files for.

        Returns:
            list (File): A list of ``File`` objects.
            object: A generic object containing paging information for the query.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        kwargs = {
            'ts_from': ts_from,
            'ts_to': ts_to,
            'types': types,
            'count': count,
            'page': page
        }

        if user is not None:
            args['user'] = user.id
        if channel is not None:
            args['channel'] = channel.id

        files = await async_wrapper(
            self._loop,
            self._client.api_call,
            'files.list',
            **kwargs
        )

        if files['ok']:
            return [File(self, x) for x in files['files']], Object(files['paging'])
        
        raise SlackError(files['error'])

    async def whoami(self):
        """
        Returns authentication information about the current user.

        Returns:
            object: A generic object representing the current user.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        me = await async_wrapper(
            self._loop,
            self._client.api_call,
            'auth.test'
        )

        if me['ok']:
            del me['ok']
            return Object(me)
        
        raise SlackError(me['error'])

    async def write(self, channel, text):
        """
        Writes a message to some channel.

        If you need more fine-grained control over your message,
        use ``Slack#raw_write`` instead.

        Args:
            channel (Channel): The channel to write a message to.
            text (str): The message to write.

        Returns:
            Message: A ``Message`` object representing the newly written
            message.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'chat.postMessage',
            channel=channel.id,
            text=text,
        )

        if resp['ok']:
            return Message(self, resp['message'])
        
        raise SlackError(resp['error'])

    async def raw_write(self, **kwargs):
        """
        Writes a message to some channel.
        
        This differs from ``Slack#write`` in that all arguments
        to ``Slack#raw_write`` must be handled by the user.
        With `Slack#write`, the user is only able to pass in a
        ``Channel`` object as well as some text string.

        For a full explanation of all arguments https://api.slack.com/methods/chat.postMessage

        Args:
            **kwargs: Arbitrary keyword arguments to be passed
                to Slack's `chat.postMessage` endpoint.

        Returns:
            Message: A ``Message`` object representing the newly written
            message.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'chat.postMessage',
            **kwargs
        )

        if resp['ok']:
            return Message(self, resp['message'])
        
        raise SlackError(resp['error'])

    async def delete(self, message, as_user=False):
        """
        Deletes a Slack message.

        Args:
            message (Message): The message to delete. This should
                be a ``Message`` object.
            as_user (bool): Whether or no to deleted the message
                as the currently authenticated user.

                Defaults to False.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'chat.delete',
            channel=message.channel,
            ts=message.ts,
            as_user=as_user
        )

        raise SlackError(resp['error'])

    async def edit(self, message, text):
        """
        Updates a message's contents.

        If you need more fine-grained control over your message,
        use ``Slack#raw_edit`` instead.

        Args:
            message (Message): The message to update. This should
                be a ``Message`` object.
            text (str): The new text to use as the message contents.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'chat.update',
            ts=message.ts,
            channel=message.channel,
            text=text
        )

        if resp['ok']:
            del resp['ok']
            return Object(resp)

        raise SlackError(resp['error'])

    async def raw_edit(self, **kwargs):
        """
        Updates a message's contents.

        This differs from ``Slack#edit`` in that all arguments
        to ``Slack#raw_edit`` must be handled by the user.
        With ``Slack#edit``, the user is only able to pass in a
        ``Message`` object as well as some text string.

        For a full explanation of all arguments https://api.slack.com/methods/chat.update

        Args:
            **kwargs: Additional options to use when updating the message.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'chat.update',
            **kwargs
        )

        if resp['ok']:
            del resp['ok']
            return Object(resp)

        raise SlackError(resp['error'])

    async def get_channel_history(self, channel, latest='now', oldest=0, inclusive=True, count=100):
        """
        Fetches and returns the message history for a channel.

        Args:
            channel (Channel): The channel to fetch the message history for.
            latest (float | ``now``): The end of time range of messages to include.
                This can be a float or ``now``. If ``now`` is specified then the current
                time is used.
                Defaults to ``now``.
            oldest (float): The start of time range of messages to include.
                Defaults to 0.
            inclusive (bool): Whether or not to include messages with latest of
                oldest timestamps.
                Defaults to True.
            count (int): The number of messages to return, between 1 and 1000.
                Defaults to 100.

        Returns:
            list (Message): A list of ``Message`` objects.
            bool: Whether or not there are more messages in the channel's history.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.history',
            channel=channel.id,
            latest=latest,
            oldest=oldest,
            inclusive=inclusive,
            count=count
        )

        if resp['ok']:
            return [Message(self, x) for x in resp['messages']], resp['has_more']

        raise SlackError(resp['error'])

    async def archive_channel(self, channel):
        """
        Archives a channel.

        Args:
            channel (Channel): The channel to archive.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.archive',
            channel=channel.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def channel_invite_user(self, channel, user):
        """
        Invites a user to join a channel.

        Args:
            channel (Channel): The channel to invite the user to.
            user (User): The user to invite to the channel.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.invite',
            channel=channel.id
        )

        if resp['ok']:
            return Channel(self, resp['channel'])

        raise SlackError(resp['error'])

    async def join_channel(self, channel):
        """
        Joins a specific channel.

        In the event that the channel is already joined, then `True`
        is returned instead of a ``Channel`` object for the joined
        channel.

        Args:
            channel (Channel): The channel to join. This channel
                must not be private.

        Returns:
            Channel: If the user has not yet joined this channel
                then a ``Channel`` object representing the newly
                joined channel will be returned.

                If the channel to join has already been joined,
                then True will be returned instead.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.join',
            name=channel.name
        )

        if resp['ok']:
            if resp.get('already_in_channel', default=False):
                return True
            return Channel(self, resp['channel'])
        
        raise SlackError(resp['error'])

    async def channel_kick(self, channel, user):
        """
        Kicks a user from a channel.

        Args:
            channel (Channel): The channel to kick the user from.
            user (User): The user to kick from the channel.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.kick',
            channel=channel.id,
            user=user.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def leave_channel(self, channel):
        """
        Leaves a channel.

        Args:
            channel (Channel): The channel to leave.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.leave',
            channel=channel.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def mark_channel(self, channel, ts):
        """
        Changes the last-read indicator in a channel
        for the current user.

        Args:
            channel (Channel): The channel to change the last-read
                indicator for.
            ts (float): The timestamp to use when changing the
                last-read indicator.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.mark',
            channel=channel.id,
            ts=ts
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def rename_channel(self, channel, name, validate=False):
        """
        Renames a channel to something else.

        Because ``channels.rename`` does not return the updated
        channel, you should refresh your ``Channel`` object by calling
        either ``Channel#update`` or replacing it with the result of
        ``Channel#group_by_id``.

        Args:
            channel (Channel): The channel to rename.
            name (str): The new name for the channel.
            validate (bool): Whether or not to return an error instead
                of changing the new name to be valid.
                Defaults to False.

        Returns:
            str: The new name for the channel.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.rename',
            channel=channel.id,
            name=name,
            validate=validate
        )

        if resp['ok']:
            return name

        raise SlackError(resp['error'])

    async def get_channel_replies(self, channel, ts):
        """
        Fetches and returns all replies to a message within a certain
        channel.

        Args:
            channel (Channel): The channel to look in for the message.
            ts: The timestamp of the parent message to look for.

        Returns:
            list (Message):
                A list of ``Message`` objects representing a message thread.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.replies',
            channel=channel.id,
            thread_ts=ts
        )

        if resp['ok']:
            return [Message(self, x) for x in resp['messages']]

        raise SlackError(resp['error'])

    async def set_channel_purpose(self, channel, purpose):
        """
        Changes the purpose of a channel.

        Because ``channels.setPurpose`` does not return the updated
        channel, you should refresh your ``Channel`` object by calling
        either ``Channel#update`` or replacing it with the result of
        ``Slack#channel_by_id``.

        Args:
            channel (Channel): The channel to change the purpose for.
            purpose (str): The new purpose for the channel as a string.

        Returns:
            str: The new channel purpose.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.setPurpose',
            channel=channel.id,
            purpose=purpose
        )

        if resp['ok']:
            return purpose
        
        raise SlackError(resp['error'])

    async def set_channel_topic(self, channel, topic):
        """
        Changes the topic of a channel.

        Because ``channels.setTopic`` does not return the updated
        channel, you should refresh your ``Channel`` object by calling
        either ``Channel#update`` or replacing it with the result of
        ``Slack#channel_by_id``.

        Args:
            channel (Channel): The channel to change the topic for.
            topic (str): The new topic for the channel as a string.

        Returns:
            str: The new channel topic.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.setTopic',
            channel=channel.id,
            topic=topic
        )

        if resp['ok']:
            return topic

        raise SlackError(resp['error'])

    async def unarchive_channel(self, channel):
        """
        Unarchives a channel.

        Args:
            channel (Channel): The channel to unarchive.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.unarchive',
            channel=channel.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])
    
    async def archive_group(self, group):
        """
        Archives a group.

        Args:
            group (Group): The channel to archive.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.archive',
            channel=group.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def close_group(self, group):
        """
        Closes a group.

        Args:
            group (Group): The group to close.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.close',
            channel=group.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def create_group_child(self, group):
        """
        Clones a group and then archives the original.

        Args:
            group (Group): The group to clone and archive.

        Returns:
            Group:
                A ``Group`` object that is a clone of the original group.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.createChild',
            channel=group.id
        )

        if resp['ok']:
            return Group(resp['group'])

        raise SlackError(resp['error'])

    async def get_group_history(self, group, latest='now', oldest=0, inclusive=True, count=100):
        """
        Fetches and returns the message history for a group.

        Args:
            group (Group): The group to fetch the message history for.
            latest (float | ``now``): The end of time range of messages to include.
                This can be a float or ``now``. If ``now`` is specified then the current
                time is used.
                Defaults to ``now``.
            oldest (float): The start of time range of messages to include.
                Defaults to 0.
            inclusive (bool): Whether or not to include messages with latest of
                oldest timestamps.
                Defaults to True.
            count (int): The number of messages to return, between 1 and 1000.
                Defaults to 100.

        Returns:
            list (Message): A list of ``Message`` objects.
            bool: Whether or not there are more messages in the group's history.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.history',
            channel=group.id,
            latest=latest,
            oldest=oldest,
            inclusive=inclusive,
            count=count
        )

        if resp['ok']:
            return [Message(self, x) for x in resp['messages']], resp['has_more']

        raise SlackError(resp['error'])

    async def group_invite_user(self, group, user):
        """
        Invites a user to join a group.

        Args:
            group (Group): The channel to invite the user to.
            user (User): The user to invite to the group.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.invite',
            channel=group.id,
            user=user.id
        )

        if resp['ok']:
            return Group(resp['group'])

        raise SlackError(resp['error'])

    async def group_kick(self, group, user):
        """
        Kicks a user from a group.

        Args:
            group (Group): The group to kick the user from.
            user (User): The user to kick from the group.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.kick',
            channel=group.id,
            user=user.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def leave_group(self, group):
        """
        Leaves a group.

        Args:
            group (Group): The group to leave.
        
        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.leave',
            channel=group.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def mark_group(self, group, ts):
        """
        Changes the last-read indicator in a group
        for the current user.

        Args:
            group (Group): The group to change the last-read
                indicator for.
            ts (float): The timestamp to use when changing the
                last-read indicator.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.mark',
            channel=group.id,
            ts=ts
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def open_group(self, group):
        """
        Opens a group channel.

        Args:
            group (Group): The group to open.

        Raises:
            SlackError: Raised in the vent that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.open',
            channel=group.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def rename_group(self, group, name, validate=False):
        """
        Renames a group to something else.

        Because ``groups.rename`` does not return the updated
        group, you should refresh your ``Group`` object by calling
        either ``Group#update`` or replacing it with the result of
        ``Slack#group_by_id``.

        Args:
            group (Group): The group to rename.
            name (str): The new name for the group.
            validate (bool): Whether or not to return an error instead
                of changing the new name to be valid.
                Defaults to False.

        Returns:
            str: The new name for the group.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.rename',
            channel=group.id,
            name=name,
            validate=validate
        )

        if resp['ok']:
            return name

        raise SlackError(resp['error'])

    async def get_group_replies(self, group, ts):
        """
        Fetches and returns all replies to a message within a certain
        group.

        Args:
            group (Group): The group to look in for the message.
            ts: The timestamp of the parent message to look for.

        Returns:
            list (Message): A list of ``Message`` objects representing a message
                thread.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'group.replies',
            channel=group.id,
            thread_ts=ts
        )

        if resp['ok']:
            return [Message(self, x) for x in resp['messages']]

        raise SlackError(resp['error'])

    async def set_group_purpose(self, group, purpose):
        """
        Changes the purpose of a group.

        Because ``groups.setPurpose`` does not return the updated
        group, you should refresh your ``Group`` object by calling
        either ``Group#update`` or replacing it with the result of
        ``Slack#group_by_id``.

        Args:
            group (Group): The groupel to change the purpose for.
            purpose (str): The new purpose for the group as a string.

        Returns:
            str: The new group purpose.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.setPurpose',
            channel=group.id,
            purpose=purpose
        )

        if resp['ok']:
            return purpose

        raise SlackError(resp['error'])

    async def set_group_topic(self, group, topic):
        """
        Changes the topic of a group.

        Because ``groups.setTopic`` does not return the updated
        group, you should refresh your ``Group`` object by calling
        either ``Group#update`` or replacing it with the result of
        ``Slack#group_by_id``.

        Args:
            group (Group): The groupel to change the purpose for.
            topic (str): The new topic for the group as a string.

        Returns:
            str: The new group topic.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.setPurpose',
            channel=group.id,
            topic=topic
        )

        if resp['ok']:
            return topic

        raise SlackError(resp['error'])

    async def unarchive_group(self, group):
        """
        Unarchives a group channel.

        Args:
            group (Group): The group to unarchive.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.unarchive',
            channel=group.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def close_im(self, im):
        """
        Closes an IM channel.

        Args:
            im (IM): The IM channel to close.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'im.close',
            channel=im.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def get_im_history(self, im, latest='now', oldest=0, inclusive=True, count=100):
        """
        Fetches and returns the message history for an IM.

        Args:
            im (IM): The IM to fetch the message history for.
            latest (float | ``now``): The end of time range of messages to include.
                This can be a float or ``now``. If ``now`` is specified then the current
                time is used.
                Defaults to ``now``.
            oldest (float): The start of time range of messages to include.

                Defaults to 0.
            inclusive (bool): Whether or not to include messages with latest of
                oldest timestamps.
                Defaults to True.
            count (int): The number of messages to return, between 1 and 1000.
                Defaults to 100.

        Returns:
            list (Message): A list of ``Message`` objects.
            bool: Whether or not there are more messages in the IM's history.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'im.history',
            channel=im.id,
            latest=latest,
            oldest=oldest,
            inclusive=inclusive,
            count=count
        )

        if resp['ok']:
            return [Message(self, x) for x in resp['messages']], resp['has_more']

        raise SlackError(resp['error'])

    async def mark_im(self, im, ts):
        """
        Changes the last-read indicator in an IM
        for the current user.

        Args:
            im (IM): The IM to change the last-read
                indicator for.
            ts (float): The timestamp to use when changing the
                last-read indicator.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'im.mark',
            channel=im.id,
            ts=ts
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def open_im(self, user):
        """
        Opens a new IM with another user.

        If an IM with the specified user is already open, then
        nothing happens.

        Args:
            user (User): The user to start an IM with.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'im.open',
            user=user.id,
            return_im=True
        )

        if resp['ok']:
            return IM(self, resp['channel'])

        raise SlackError(resp['error'])

    async def get_im_replies(self, im, ts):
        """
        Fetches and returns all replies to a message within a certain IM.

        Args:
            im (IM): The IM to look in for the message.
            ts: The timestamp of the parent message to look for.

        Returns:
            list (Message):
                A list of ``Message`` objects representing a message thread.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'im.replies',
            channel=im.id,
            thread_ts=ts
        )

        if resp['ok']:
            return [Message(self, x) for x in resp['messages']]

        raise SlackError(resp['error'])

    async def close_mpim(self, mpim):
        """
        Closes a MPIM.

        Args:
            mpim (MPIM): The MPIM to close.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'mpim.close',
            channel=mpim.id,
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def get_mpim_history(self, im, latest='now', oldest=0, inclusive=True, count=100):
        """
        Fetches and returns the message history for a MPIM.

        Args:
            mpim (MPIM): The MPIM to fetch the message history for.
            latest (float | ``now``): The end of time range of messages to include.
                This can be a float or ``now``. If ``now`` is specified then the current
                time is used.
                Defaults to ``now``.
            oldest (float): The start of time range of messages to include.
                Defaults to 0.
            inclusive (bool): Whether or not to include messages with latest of
                oldest timestamps.
                Defaults to True.
            count (int): The number of messages to return, between 1 and 1000.
                Defaults to 100.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'mpim.history',
            channel=mpim.id,
            latest=latest,
            oldest=oldest,
            inclusive=inclusive,
            count=count
        )

        if resp['ok']:
            return [Message(self, x) for x in resp['messages']], resp['has_more']

        raise SlackError(resp['error'])

    async def mark_mpim(self, mpim, ts):
        """
        Changes the last-read indicator in a MPIM
        for the current user.

        Args:
            mpim (MPIM): The MPIM to change the last-read
                indicator for.
            ts (float): The timestamp to use when changing the
                last-read indicator.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'mpim.mark',
            channel=mpim.id,
            ts=ts
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def get_mpim_history(self, mpim, latest='now', oldest=0, inclusive=True, count=100):
        """
        Fetches and returns the message history for an MPIM.

        Args:
            mpim (MPIM): The MPIM to fetch the message history for.
            latest (float | ``now``): The end of time range of messages to include.
                This can be a float or ``now`.` If ``now`` is specified then the current
                time is used.
                Defaults to ``now``.
            oldest (float): The start of time range of messages to include.
                Defaults to 0.
            inclusive (bool): Whether or not to include messages with latest of
                oldest timestamps.
                Defaults to True.
            count (int): The number of messages to return, between 1 and 1000.
                Defaults to 100.

        Returns:
            list (Message): A list of ``Message`` objects.
            bool: Whether or not there are more messages in the MPIM's history.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'mpim.history',
            channel=im.id,
            latest=latest,
            oldest=oldest,
            inclusive=inclusive,
            count=count
        )

        if resp['ok']:
            return [Message(self, x) for x in resp['messages']], resp['has_more']

        raise SlackError(resp['error'])

    async def open_mpim(self, *users):
        """
        Opens an MPIM with multiple users.

        Args:
            *users (User): A variadic list of ``User`` objects to
                start an MPIM with.

        Returns:
            MPIM: The newly created MPIM channel.

        Raises:
            SlackError: Raised in the vent that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'mpim.open',
            users=','.join(x.id for x in users)
        )

        if resp['ok']:
            return MPIM(self, resp['channel'])

        raise SlackError(resp['error'])

    async def get_mpim_replies(self, mpim, ts):
        """
        Fetches and returns all replies to a message within a certain MPIM.

        Args:
            mpim (MPIM): The MPIM to look in for the message.
            ts: The timestamp of the parent message to look for.

        Returns:
            list (Message):
                A list of ``Message`` objects representing a message thread.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'mpim.replies',
            channel=mpim.id,
            thread_ts=ts
        )

        if resp['ok']:
            return [Message(self, x) for x in resp['messages']]

        raise SlackError(resp['error'])

    async def add_message_reaction(self, message, name):
        """
        Adds a reaction to a message.

        Args:
            message (Message): The message to add a reaction to.
            name (str): The name of the reaction to add.
                A list of standard Slack reactions/emoji can be found at
                https://www.webpagefx.com/tools/emoji-cheat-sheet/.
                
        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'reactions.add',
            channel=message.channel,
            timestamp=message.ts,
            name=name
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def get_message_reactions(self, message):
        """
        Fetches and returns a list of all emoji for a message.

        Args:
            message (Message): The message to get reactions for.

        Returns:
            list (Object): A list of generic objects with reaction data.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'reactions.get',
            channel=message.channel,
            timestamp=message.ts,
            full=True # always get the full list
        )

        if resp['ok']:
            return [Object(x) for x in resp['message']['reactions']]            

        raise SlackError(resp['error'])

    async def remove_message_reaction(self, message, name):
        """
        Removes a reaction from a message.

        Args:
            message (Message): The message to remove a reaction from.
            name (str): The name of the reaction to remove.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'reactions.remove',
            channel=message.channel,
            timestamp=message.ts,
            name=name
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def add_file_reaction(self, file, name):
        """
        Adds a reaction to a file.

        Args:
            file (File): The file to add a reaction to.
            name (str): The name of the reaction to add.
                A list of standard Slack reactions/emoji can be found at
                https://www.webpagefx.com/tools/emoji-cheat-sheet/.
                
        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'reactions.add',
            file=file.id,
            name=name
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def get_file_reactions(self, file):
        """
        Fetches and returns a list of all reactions for a file.

        Args:
            file (File): The file to get reactions for.

        Returns:
            list (Object): A list of generic objects with reaction data.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'reactions.get',
            file=file.id,
            full=True # always get the full list
        )

        if resp['ok']:
            return [Object(x) for x in resp['file']['reactions']]

        raise SlackError(resp['error'])

    async def remove_file_reaction(self, file):
        """
        Removes a reaction from a file.

        Args:
            file (File): The file to remove a reaction from.
            name (str): The name of the reaction to remove.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'reactions.remove',
            file=file.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def delete_file(self, file):
        """
        Deletes a file from the Slack team.

        Args:
            file (File): The file to delete.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'files.delete',
            file=file.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def revoke_file(self, file):
        """
        Revokes a file from being shared publicly.

        Args:
            file (File): The file to revoke.

        Returns:
            File: An updated ``File`` object without the public URL for
                the file.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'files.revokePublicURL',
            file=file.id
        )

        if resp['ok']:
            return File(self, resp['file'])
        
        raise SlackError(resp['error'])

    async def share_file(self, file):
        """
        Creates a public URL for a file.

        Args:
            file (File): The file to share.

        Returns:
            File: An updated ``File`` object with the public URL for
                the file.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'files.sharedPublicURL',
            file=file.id
        )

        if resp['ok']:
            return File(self, resp['file'])
        
        raise SlackError(resp['error'])

    async def upload_file(self, filename, *channels, **kwargs):
        """
        Uploads a file and shares it with some channels.

        Args:
            filename (str): The name of the file.
            *channels (Channel): A variadic list containing ``Channel`` objects.
                The uploaded file will be shared to all these channels.
            **kwargs: Additonal arguments to pass to Slack's `files.upload` endpoint.
                Refer to https://api.slack.com/methods/files.upload for more information.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'files.upload',
            filename=filename,
            channels=','.join([x.id for x in channels]),
            **kwargs
        )

        if resp['ok']:
            return File(self, resp['file'])

        raise SlackError(resp['error'])

    async def get_file_comments(self, file, count=100, page=1):
        """
        Fetches and returns the comments for an uploaded file.

        Args:
            file (File): The file to fetch comments for.
            count (int): The number of comments per page to return.
                Defaults to 100.
            page (int): The comments page number to use.
                Defaults to 1

        Returns:
            list<Comment>: A list of ``Comment`` objects for the query.
            object: A generic object containing paging information.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'files.info',
            file=file.id,
            count=count,
            page=page
        )

        if resp['ok']:
            return [Comment(self, x, file) for x in resp['comments']], Object(resp['paging'])

        raise SlackError(resp['error'])

    async def add_file_comment(self, file, comment):
        """
        Adds a comment to a file.

        Args:
            file (File): The file to add a comment to.
            comment (str): The comment string.

        Returns:
            Comment: A ``Comment`` object representing the new comment.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'files.comments.add',
            file=file.id,
            comment=comment
        )

        if resp['ok']:
            return Comment(self, resp['comment'], file)

        raise SlackError(resp['error'])

    async def delete_file_comment(self, comment):
        """
        Deletes a comment from a file.

        Args:
            comment (Comment): The comment to delete.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'files.comments.delete',
            file=comment._file.id,
            comment=comment.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def edit_file_comment(self, comment, text):
        """
        Edits a comment's text.'

        Args:
            comment (Comment): The comment to edit.
            text (str): The new comment text.

        Returns:
            Comment: A ``Comment`` object representing the new comment.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'files.comments.edit',
            file=comment._file.id,
            id=comment.id,
            comment=text
        )

        if resp['ok']:
            return Comment(self, resp, file)
        
        raise SlackError(resp['error'])

    ########################################
    # UTILITY FUNCTIONS
    ########################################

    def format_timestamp(self, ms):
        """
        Formats a Slack timestamp and returns a
        ``datetime`` object.

        Args:
            ms (str|int|float): A Slack timestamp to format.

        Returns:
            datetime: A datetime representation of the provided timestamp.
        """
        epoch = datetime(1970, 1, 1)
        return epoch + timedelta(seconds=ms)

    async def _read(self):
        while True: 
            rtm_output = await async_wrapper(self._loop, self._client.rtm_read)

            if len(rtm_output) == 0:
                continue

            yield [line for line in rtm_output]

    def handle(self, evt):
        """
        Decorator for setting a function as an event
        handler for a Slack event.

        Args:
            evt (str): The event name to hook.
        """
        def dec(fn):
            nonlocal evt
            if evt in self._listeners:
                self._listeners[evt].append(fn)
            else:
                self._listeners[evt] = [fn]
            return fn
        return dec

    def on(self, evt, fn):
        """
        Adds a function to the list of event handlers for a
        particular event.

        Args:
            evt (str): The event to hook.
            fn (Function): The function to execute when the specified
                event is received.

        Returns:
            int: The index of the added handler in the list of handlers.
                This is used when removing event handlers.
        """
        if evt in self._listeners:
            self._listeners[evt].append(fn)
        else:
            self._listeners[evt] = [fn]
        
        return len(self._listeners[evt])

    def off(self, evt, index):
        """
        Removes a function from the list of event handlers for a
        particular event.

        Args:
            evt (str): The event to remove the listener from.
            index (int): The index number of the event handler
                in the list of event handlers.
        """
        if evt in self._listeners:
            self._listeners.pop(index)

    def transform(self, evt, fn):
        """
        Sets the transformation function for an event.
        This **should not** be used unless you know what you are doing.

        Args:
            evt (str): The name of the event to set the transformation
                function for.
            fn (Function): The transformation function to use.
        """
        self._transforms[evt] = fn

    async def listen(self):
        """
        Initializes a connection to Slack RTM.
        """
        self._loop = asyncio.get_event_loop()
        self.me = await self.whoami()

        print('Using user "{}" with ID {}.'.format(self.me.user, self.me.user_id))

        if not self._client.rtm_connect():
            print('Failed to connect to Slack RTM.')
            return

        print('Connected to Slack RTM.')

        startup = datetime.utcnow()

        async for output in self._read():
            for line in output:
                if line['type'] in self._listeners:
                    if line['type'] in self._transforms:
                        line = await self._transforms[line['type']](line)
                    else:
                        line = Object(line)

                    # Convert Slack timestamps to datetime objects.
                    if getattr(line, 'ts', None) is not None:
                        ts = self._format_timestamp(float(line.ts))

                        # ignore messages from the past.
                        if ts < startup:
                            continue

                    for fn in self._listeners[line.type]:
                        await fn(line)

    def set_token(self, token):
        """
        Sets the current Slack token.

        Args:
            token (str): The Slack token to use.
        """
        self._client = SlackClient(token)

    def start(self):
        """
        Initializes a Slack RTM connection and begins listening to it.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.listen())