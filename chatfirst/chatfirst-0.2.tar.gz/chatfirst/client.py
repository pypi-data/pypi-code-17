from chatfirst import ChatfirstClient
from chatfirst.models import Bot, Channel, ActionResponse


__author__ = 'it@chatfirst.co (Ivan Tertychnyy)'

class Chatfirst:
    """
    The Chatfirst class is a wrapper of `Chatfirst API <https://api.chatfirst.co>`_
    This class provides easy access to `bots, push, talk, broadcast methods <https://api.chatfirst.co/swagger>`_

    :param token: user's token from Chatfirst dashboard
    :type token: str
    """
    def __init__(self, token):
        self.token = token
        self.client = ChatfirstClient(token, secure=True)

    def bots_list(self):
        """
        List all user's bots

        :rtype: list of Bot
        :return: user's bots
        """
        data = self.client.bots()
        return [Bot(item) for item in data]

    def bots_create(self, bot):
        """
        Save new bot

        :param bot: bot object to save
        :type bot: Bot
        """
        self.client.bots(_method="POST", _json=bot.to_json(), _params=dict(userToken=self.token))

    def bots_get(self, bot):
        """
        Fetch and fill Bot object

        :param bot: empty bot object with name to search
        :type bot: Bot
        :rtype: Bot
        :return: filled bot object
        """
        data = self.client.bots.__getattr__(bot.name).__call__()
        return Bot(data)

    def bots_update(self, bot):
        """
        Update Bot

        :param bot: bot object to update
        :type bot: Bot
        """
        self.client.bots.__getattr__(bot.name).__call__(_method="PUT", _json=bot.to_json(), _params=dict(botName=bot.name))

    def bots_delete(self, bot):
        """
        Delete existing bot

        :param bot: bot to delete
        :type bot: Bot
        """
        self.client.bots.__getattr__(bot.name).__call__(_method="DELETE", _params=dict(botName=bot.name))

    def channels_link(self, bot, channel, channel_type):
        params = dict()
        params["channel"] = channel_type
        params["externalToken"] = channel.token
        params["botName"] = bot.name
        self.client.channels.link(_method="PUT", _params=params)

    def channels_unlink(self, bot, channel_type):
        params = dict()
        params["channel"] = channel_type
        params["botName"] = bot.name
        self.client.channels.unlink(_method="PUT", _params=params)

    def channels_force(self, bot, channel_type, state):
        self.client.channels.force.__getattr__(bot.name).__getattr__(channel_type).__call__(_method="PUT", _params=dict(state=state))

    def channels_get(self, bot, channel_type):
        data = self.client.channels(_method="GET", _params=dict(channel=channel_type, botName=bot.name))
        return Channel(data)

    def talk(self, bot, message):
        """
        Talk to bot and get response based
        You can use this method to integrate the platform with your own channels

        :param bot: bot to talk to
        :type bot: Bot
        :param message: message to send to bot
        :type message: Message
        :rtype: ActionResponse
        :return: response object
        """
        data = self.client.talk(_method="POST", _params=dict(botName=bot.name), _json=message.to_json())
        return ActionResponse(data)

    def push(self, bot, channel_type, ar, user_id):
        """
        Use this method to push message to user of bot.
        The message should be packed into ActionResponse object.
        This allows to push text messages, buttons, images.
        This also allows to force current state of user.

        :param bot: bot that will push user
        :type bot: Bot
        :param channel_type: one of [telegram, facebook, slack]
        :type channel_type: str
        :param ar: message packed in response object
        :type ar: ActionResponse
        :param user_id: user id in used channel
        :type user_id: str
        """
        self.client.push.__getattr__(bot.name).__call__(_method="POST",
                                                        _params=dict(id=user_id, channel=channel_type),
                                                        _json=ar.to_json())

    def broadcast(self, bot, channel_type, text):
        """
        Use this method to broadcast text message to all users of bot.

        :param bot: bot that will push user
        :type bot: Bot
        :param channel_type: one of [telegram, facebook, slack]
        :type channel_type: str
        :param text: text message
        :type text: str
        """
        self.client.broadcast.__getattr__(bot.name).__call__(_method="POST",
                                                        _params=dict(channel=channel_type),
                                                        _json=dict(message=text))
