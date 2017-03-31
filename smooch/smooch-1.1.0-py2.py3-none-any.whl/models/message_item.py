# coding: utf-8

"""
    Smooch

    The Smooch API is a unified interface for powering messaging in your customer experiences across every channel. Our API speeds access to new markets, reduces time to ship, eliminates complexity, and helps you build the best experiences for your customers. For more information, visit our [official documentation](https://docs.smooch.io).

    OpenAPI spec version: 1.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class MessageItem(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, title=None, description=None, media_url=None, size=None, media_type=None, actions=None):
        """
        MessageItem - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'title': 'str',
            'description': 'str',
            'media_url': 'str',
            'size': 'str',
            'media_type': 'str',
            'actions': 'list[Action]'
        }

        self.attribute_map = {
            'title': 'title',
            'description': 'description',
            'media_url': 'mediaUrl',
            'size': 'size',
            'media_type': 'mediaType',
            'actions': 'actions'
        }

        self._title = title
        self._description = description
        self._media_url = media_url
        self._size = size
        self._media_type = media_type
        self._actions = actions

    @property
    def title(self):
        """
        Gets the title of this MessageItem.
        The title of the message item.

        :return: The title of this MessageItem.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this MessageItem.
        The title of the message item.

        :param title: The title of this MessageItem.
        :type: str
        """
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")

        self._title = title

    @property
    def description(self):
        """
        Gets the description of this MessageItem.
        The text description, or subtitle.

        :return: The description of this MessageItem.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this MessageItem.
        The text description, or subtitle.

        :param description: The description of this MessageItem.
        :type: str
        """

        self._description = description

    @property
    def media_url(self):
        """
        Gets the media_url of this MessageItem.
        The image URL to be shown in the carousel/list item.

        :return: The media_url of this MessageItem.
        :rtype: str
        """
        return self._media_url

    @media_url.setter
    def media_url(self, media_url):
        """
        Sets the media_url of this MessageItem.
        The image URL to be shown in the carousel/list item.

        :param media_url: The media_url of this MessageItem.
        :type: str
        """

        self._media_url = media_url

    @property
    def size(self):
        """
        Gets the size of this MessageItem.
        The size of the image to be shown in the carousel/list item. Only top item of Facebook Messenger carousel supported. Choose from *compact* and *large*. 

        :return: The size of this MessageItem.
        :rtype: str
        """
        return self._size

    @size.setter
    def size(self, size):
        """
        Sets the size of this MessageItem.
        The size of the image to be shown in the carousel/list item. Only top item of Facebook Messenger carousel supported. Choose from *compact* and *large*. 

        :param size: The size of this MessageItem.
        :type: str
        """

        self._size = size

    @property
    def media_type(self):
        """
        Gets the media_type of this MessageItem.
        If a *mediaUrl* was specified, the media type is defined here, for example *image/jpeg*.

        :return: The media_type of this MessageItem.
        :rtype: str
        """
        return self._media_type

    @media_type.setter
    def media_type(self, media_type):
        """
        Sets the media_type of this MessageItem.
        If a *mediaUrl* was specified, the media type is defined here, for example *image/jpeg*.

        :param media_type: The media_type of this MessageItem.
        :type: str
        """

        self._media_type = media_type

    @property
    def actions(self):
        """
        Gets the actions of this MessageItem.
        Array of [action buttons](https://docs.smooch.io/rest/#action-buttons). At least 1 is required, a maximum of 3 are allowed.

        :return: The actions of this MessageItem.
        :rtype: list[Action]
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """
        Sets the actions of this MessageItem.
        Array of [action buttons](https://docs.smooch.io/rest/#action-buttons). At least 1 is required, a maximum of 3 are allowed.

        :param actions: The actions of this MessageItem.
        :type: list[Action]
        """
        if actions is None:
            raise ValueError("Invalid value for `actions`, must not be `None`")

        self._actions = actions

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, MessageItem):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
