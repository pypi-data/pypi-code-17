import asyncio
from datetime import datetime, timedelta
import json
from slackclient import SlackClient
from .lib.async import async_wrapper
from .lib.object import Object

from .lib.slackerror import SlackError

from .lib.channel import Channel
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
        group = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.info',
            group=id
        )

        if group['ok']:
            return Group(self, group['group'])

        raise SlackError(channel['error'])

    async def user_by_id(self, uid):
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
        bot = await async_wrapper(
            self._loop,
            self._client.api_call,
            'bot.info',
            bot=bid
        )

        if bot['ok']:
            return User(self, bot['bot'])
        
        raise SlackError(bot['error'])

    async def create_channel(self, name, validate=False):
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
        ims = await async_wrapper(
            self._loop,
            self._client.api_call,
            'im.list'
        )

        if ims['ok']:
            return [IM(self, x) for x in ims['ims']]

        raise SlackError(ims['error'])

    async def list_mpims(self):
        groups = await async_wrapper(
            self._loop,
            self._client.api_call,
            'mpim.list',
        )

        if groups['ok']:
            return [Group(self, x) for x in groups['groups']]

        raise SlackError(groups['error'])

    async def list_users(self, presence=True):
        users = await async_wrapper(
            self._loop,
            self._client.api_call,
            'users.list',
            presence=presence
        )
        
        if users['ok']:
            return [User(self, x) for x in users['members']]
        
        raise SlackError(users.users)

    async def whoami(self):
        me = await async_wrapper(
            self._loop,
            self._client.api_call,
            'auth.test'
        )

        if me['ok']:
            return Object(me)
        
        raise SlackError(me['error'])

    async def write(self, **kwargs):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'chat.postMessage',
            **kwargs
        )

        if resp['ok']:
            return Message(self, resp['message'])
        
        raise SlackError(resp['error'])

    async def delete(self, message, as_user=True):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'chat.delete',
            channel=message.channel,
            ts=message.ts,
            as_user=as_user
        )

        raise SlackError(resp['error'])

    async def edit(self, text, **kwargs):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'chat.update',
            text,
            **kwargs
        )

        if resp['ok']:
            del resp['ok']
            return Object(resp)

        raise SlackError(resp['error'])

    async def get_channel_history(self, channel, **kwargs):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.history',
            channel=channel.id,
            **kwrags
        )

        if resp['ok']:
            # If we reached here then everything is ok.
            # User should not need to check for "ok" so
            # we are deleting this for them.
            del resp['ok']
            resp['messages'] = [Message(self, x) for x in resp['messages']]
            return Object(resp)

        raise SlackError(resp['error'])

    async def archive_channel(self, channel):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.archive',
            channel=channel.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def channel_invite_user(self, channel, user):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.invite',
            channel=channel.id
        )

        if resp['ok']:
            return Channel(self, resp['channel'])

        raise SlackError(resp['error'])

    async def join_channel(self, channel, validate=False):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.join',
            name=channel.name,
            validate=validate
        )

        if resp['ok']:
            return Channel(self, resp['channel'])
        
        raise SlackError(resp['error'])

    async def channel_kick(self, channel, user):
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
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.leave',
            channel=channel.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def mark_channel(self, channel, ts):
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
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.rename',
            channel=channel.id,
            name=name,
            validate=validate
        )

        if resp['ok']:
            return Channel(self, resp['channel'])

        raise SlackError(resp['error'])

    async def get_channel_replies(self, channel, ts):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.replies',
            channel=channel.id,
            thread_ts=ts
        )

        if resp['ok']:
            del resp['ok']
            resp['messages'] = [Message(self, x) for x in resp['messages']]
            return Object(resp)

        raise SlackError(resp['error'])

    async def set_channel_purpose(self, channel, purpose):
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
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.unarchive',
            channel=channel.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])
    
    async def archive_group(self, group):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.archive',
            channel=group.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def close_group(self, group):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.close',
            channel=group.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def create_group_child(self, group):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.createChild',
            channel=group.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def get_group_history(self, group, **kwargs):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.history',
            channel=group.id,
            **kwrags
        )

        if resp['ok']:
            # If we reached here then everything is ok.
            # User should not need to check for "ok" so
            # we are deleting this for them.
            del resp['ok']
            resp['messages'] = [Message(self, x) for x in resp['messages']]
            return Object(resp)

        raise SlackError(resp['error'])

    async def group_invite_user(self, group, user):
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
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.leave',
            channel=group.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def mark_group(self, group, ts):
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
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.open',
            channel=group.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def rename_group(self, group, name, validate=False):
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
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'group.replies',
            channel=group.id,
            thread_ts=ts
        )

        if resp['ok']:
            del resp['ok']
            resp['messages'] = [Message(self, x) for x in resp['messages']]
            return Object(resp)

        raise SlackError(resp['error'])

    async def set_group_purpose(self, group, purpose):
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
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.unarchive',
            channel=group.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def close_im(self, im):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'im.close',
            channel=im.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def get_im_history(self, im, **kwargs):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'im.history',
            channel=im.id,
            **kwrags
        )

        if resp['ok']:
            del resp['ok']
            resp['messages'] = [Message(self, x) for x in resp['messages']]
            return Object(resp)

        raise SlackError(resp['error'])

    async def mark_im(self, im, ts):
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
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'im.open',
            user=user.id
        )

        if resp['ok']:
            return IM(self, resp['channel'])

        raise SlackError(resp['error'])

    async def get_im_replies(self, im, ts):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'im.replies',
            channel=im.id,
            thread_ts=ts
        )

        if resp['ok']:
            del resp['ok']
            resp['messages'] = [Message(self, x) for x in resp['messages']]
            return Object(resp)

        raise SlackError(resp['error'])

    async def close_mpim(self, mpim):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'mpim.close',
            channel=mpim.id,
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def get_mpim_history(self, mpim, **kwargs):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'mpim.history',
            channel=mpim.id,
            **kwrags
        )

        if resp['ok']:
            del resp['ok']
            resp['messages'] = [Message(self, x) for x in resp['messages']]
            return Object(resp)

        raise SlackError(resp['error'])

    async def mark_mpim(self, mpim, ts):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'mpim.mark',
            channel=mpim.id,
            ts=ts
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def open_mpim(self, user):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'mpim.open',
            user=user.id
        )

        if resp['ok']:
            return MPIM(self, resp['channel'])

        raise SlackError(resp['error'])

    async def get_mpim_replies(self, mpim, ts):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'mpim.replies',
            channel=mpim.id,
            thread_ts=ts
        )

        if resp['ok']:
            del resp['ok']
            resp['messages'] = [Message(self, x) for x in resp['messages']]
            return Object(resp)

        raise SlackError(resp['error'])

    async def add_message_reaction(self, message, name):
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
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'reactions.get',
            channel=message.channel,
            timestamp=message.ts,
            full=True # always get the full list
        )

        if resp['ok']:
            del resp['ok']
            resp['message'] = Message(self, resp['message'])
            return Object(resp)

        raise SlackError(resp['error'])

    async def remove_message_reaction(self, message):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'reactions.remove',
            channel=message.channel,
            timestamp=message.ts
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    async def add_file_reaction(self, file, name):
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
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'reactions.get',
            file=file.id,
            full=True # always get the full list
        )

        if resp['ok']:
            del resp['ok']
            resp['file'] = File(self, resp['file'])
            return Object(resp)

        raise SlackError(resp['error'])

    async def remove_file_reaction(self, file):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'reactions.remove',
            file=file.id
        )

        if not resp['ok']:
            raise SlackError(resp['error'])

    ########################################
    # UTILITY FUNCTIONS
    ########################################

    def _format_timestamp(self, ms):
        epoch = datetime(1970, 1, 1)
        return epoch + timedelta(seconds=ms)

    async def _read(self):
        while True: 
            rtm_output = await async_wrapper(self._loop, self._client.rtm_read)

            if len(rtm_output) == 0:
                continue

            yield [line for line in rtm_output]

    def on(self, evt, fn):
        if evt in self._listeners:
            self._listeners[evt].append(fn)
        else:
            self._listeners[evt] = [fn]

    def transform(self, evt, fn):
        self._transforms[evt] = fn

    async def listen(self):
        self._loop = asyncio.get_event_loop()

        print('Using user "{}" with ID {}.'.format(me.user, me.user_id))

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
                        line.ts = self._format_timestamp(float(line.ts))

                        # ignore messages from the past.
                        if line.ts < startup:
                            continue

                    for fn in self._listeners[line.type]:
                        await fn(line)

    def set_token(self, token):
        self._client = SlackClient(token)
        self.me = await self.whoami()        

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.listen())