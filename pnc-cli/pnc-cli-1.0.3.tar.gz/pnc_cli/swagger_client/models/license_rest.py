# coding: utf-8

"""
Copyright 2015 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from datetime import datetime
from pprint import pformat
from six import iteritems


class LicenseRest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        LicenseRest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'int',
            'full_name': 'str',
            'full_content': 'str',
            'ref_url': 'str',
            'short_name': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'full_name': 'fullName',
            'full_content': 'fullContent',
            'ref_url': 'refUrl',
            'short_name': 'shortName'
        }

        self._id = None
        self._full_name = None
        self._full_content = None
        self._ref_url = None
        self._short_name = None

    @property
    def id(self):
        """
        Gets the id of this LicenseRest.


        :return: The id of this LicenseRest.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this LicenseRest.


        :param id: The id of this LicenseRest.
        :type: int
        """
        self._id = id

    @property
    def full_name(self):
        """
        Gets the full_name of this LicenseRest.


        :return: The full_name of this LicenseRest.
        :rtype: str
        """
        return self._full_name

    @full_name.setter
    def full_name(self, full_name):
        """
        Sets the full_name of this LicenseRest.


        :param full_name: The full_name of this LicenseRest.
        :type: str
        """
        self._full_name = full_name

    @property
    def full_content(self):
        """
        Gets the full_content of this LicenseRest.


        :return: The full_content of this LicenseRest.
        :rtype: str
        """
        return self._full_content

    @full_content.setter
    def full_content(self, full_content):
        """
        Sets the full_content of this LicenseRest.


        :param full_content: The full_content of this LicenseRest.
        :type: str
        """
        self._full_content = full_content

    @property
    def ref_url(self):
        """
        Gets the ref_url of this LicenseRest.


        :return: The ref_url of this LicenseRest.
        :rtype: str
        """
        return self._ref_url

    @ref_url.setter
    def ref_url(self, ref_url):
        """
        Sets the ref_url of this LicenseRest.


        :param ref_url: The ref_url of this LicenseRest.
        :type: str
        """
        self._ref_url = ref_url

    @property
    def short_name(self):
        """
        Gets the short_name of this LicenseRest.


        :return: The short_name of this LicenseRest.
        :rtype: str
        """
        return self._short_name

    @short_name.setter
    def short_name(self, short_name):
        """
        Sets the short_name of this LicenseRest.


        :param short_name: The short_name of this LicenseRest.
        :type: str
        """
        self._short_name = short_name

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
	    elif isinstance(value, datetime):
		result[attr] = str(value.date())
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
