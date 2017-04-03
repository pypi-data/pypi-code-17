import json


class ActionResponse(object):
    """
    Main class defining ActionResponse entity

    :param data: serialized object
    :type data: dict
    """
    def __init__(self, data={}):
        #: ignore this parameter
        self.count = data['Count'] if 'Count' in data.keys() else None

        #: data["Messages"],
        #: list of messages to return as text messages
        self.messages = data['Messages'] if 'Messages' in data.keys() else []

        #: data["ForcedState"],
        #: forced transition to state (useful trick for scoped scenarios and error handling)
        self.forced = data['ForcedState'] if 'ForcedState' in data.keys() else None

        #: data["ForcedKeyboard"],
        #: keys to be shown to user
        self.keyboard = data['ForcedKeyboard'] if 'ForcedKeyboard' in data.keys() else None

        #: data["Entities"],
        #: list of LinkedEntity objects
        self.entities = [LinkedEntity(item) for item in data['Entities']] if 'Entities' in data.keys() else []

        #: data["ForcedMessage"],
        #: Context message
        self.forced_message = data['ForcedMessage'] if 'ForcedMessage' in data.keys() else None

    def to_json(self):
        """
        Serialize object to json dict

        :return: dict
        """
        res = dict()
        res['Count'] = self.count
        res['Messages'] = self.messages
        res['ForcedState'] = self.forced
        res['ForcedKeyboard'] = self.keyboard
        res['Entities'] = list()
        for item in self.entities:
            res['Entities'].append(item.to_json())
        res['ForcedMessage'] = self.forced_message
        return res


class ErrorResponse(ActionResponse):
    def __init__(self, message):
        ActionResponse.__init__(self)
        self.messages = [message]


class LinkedEntity:
    """
    The way to show images in bot.
    Every object will be rendered as gallery or set of image messages.

    :param data: serialized object
    :type data: dict
    """
    def __init__(self, data={}):
        #: data["Name"],
        #: name of image
        self.name = data['Name'] if 'Name' in data.keys() else None

        #: data["Description"],
        #: description of image
        self.desc = data['Description'] if 'Description' in data.keys() else None

        #: data["ImageUrl"],
        #: url of image
        self.url = data['ImageUrl'] if 'ImageUrl' in data.keys() else None

        #: data["EntityOptions"],
        #: keys to be shown to user
        self.options = data['EntityOptions'] if 'EntityOptions' in data.keys() else []

    def __str__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        """
        Serialize object to json dict

        :return: dict
        """
        res = dict()
        res['Handle'] = ''
        res['Name'] = self.name
        res['ImageUrl'] = self.url
        res['Description'] = self.desc
        res["EntityOptions"] = self.options
        return res


class Bot:
    """
    Main class defining Bot entity

    :param data: serialized object
    :type data: dict
    """
    def __init__(self, data={}):
        #: data["name"],
        #: short name of bot
        self.name = data['name'] if 'name' in data.keys() else None

        #: data["language"],
        #: 0 - Russian, 1 - English
        self.language = data['language'] if 'language' in data.keys() else None

        #: data["fancy_name"],
        #: long name of bot
        self.fancy_name = data['fancy_name'] if 'fancy_name' in data.keys() else None

        #: data["scenario"],
        #: scenario of bot
        self.scenario = data['scenario'] if 'scenario' in data.keys() else None

    def to_json(self):
        """
        Serialize object to json dict

        :return: dict
        """
        data = dict()
        data['name'] = self.name
        data['language'] = self.language
        data['fancy_name'] = self.fancy_name
        data['scenario'] = self.scenario
        return data

    def __eq__(self, other):
        if not self.name == other.name:
            return False
        if not self.language == other.language:
            return False
        if not self.fancy_name == other.fancy_name:
            return False
        if not self.scenario == other.scenario:
            return False
        return True


class Channel:
    def __init__(self, data={}):
        self.token = data['Token'] if 'Token' in data.keys() else None
        self.name = data['Name'] if 'Name' in data.keys() else None
        self.user_token = data['UserToken'] if 'UserToken' in data.keys() else None
        self.bot_name = data['BotName'] if 'BotName' in data.keys() else None

    def to_json(self):
        data = dict()
        data['Token'] = self.token
        data['Name'] = self.name
        data['UserToken'] = self.user_token
        data['BotName'] = self.bot_name
        return data

    def __eq__(self, other):
        if not type(other) == Channel:
            return False
        if not self.name == other.name:
            return False
        if not self.token == other.token:
            return False
        if not self.user_token == other.user_token:
            return False
        if not self.bot_name == other.bot_name:
            return False
        return True


class Message:
    """
    Use this class if you want to integrate your own channel and use talk method.
    Chatfirst platform accepts incomming talk requests with special json object:

    :param data: serialized object
    :type data: dict
    """
    def __init__(self, data={}):
        #: data["InterlocutorId"],
        #: internal id of talking user
        self.id_ = data['InterlocutorId'] if 'InterlocutorId' in data.keys() else None

        #: data["Text"],
        #: text message that user sent
        self.text = data['Text'] if 'Text' in data.keys() else None

        #: data["Username"],
        #: username of talking user
        self.username = data['Username'] if 'Username' in data.keys() else None

        #: data["FirstName"],
        #: first name of talking user
        self.first_name = data['FirstName'] if 'FirstName' in data.keys() else None

        #: data["LastName"],
        #: last name of talking user
        self.last_name = data['LastName'] if 'LastName' in data.keys() else None

    def to_json(self):
        """
        Serialize object to json dict

        :return: dict
        """
        data = dict()
        data['InterlocutorId'] = self.id_
        data['Text'] = self.text
        data['Username'] = self.username
        data['FirstName'] = self.first_name
        data['LastName'] = self.last_name
        return data

    def __eq__(self, other):
        if not type(other) == Message:
            return False
        if not self.id_ == other.id_:
            return False
        if not self.text == other.text:
            return False
        if not self.username == other.username:
            return False
        if not self.first_name == other.first_name:
            return False
        if not self.last_name == other.last_name:
            return False
        return True
