#! /usr/bin/env python
# coding: utf-8

import base64
import requests

from JYAliYun.Tools import ConvertObject
from JYAliYun.AliYunMNS import construct_headers
from JYAliYun.AliYunObject import ObjectManager

__author__ = 'ZhouHeng'


class MNSTopicsManager(ObjectManager):
    version = "2015-06-06"

    def __init__(self, topic_name):
        super(MNSTopicsManager, self).__init__()
        self.topic_name = topic_name
        self.message_tag = None
        self.message_attributes = None

    def publish_message(self, message_body, message_tag=None, message_attributes=None):
        message_body = base64.b64encode(ConvertObject.encode(message_body))
        data = {"MessageBody": message_body}
        if message_tag is not None:
            data["MessageTag"] = message_tag
        if message_attributes is not None:
            data["MessageAttributes"] = message_attributes
        resource = "/topics/%s/messages" % self.topic_name
        headers = construct_headers(self.access_key_id, self.access_key_secret, "POST", "text/xml;charset=utf-8",
                                    {"x-mns-version": self.version}, resource)

        xml_data = ConvertObject.dict_to_xml("Message", data)
        url = self.server_url + resource
        resp = requests.post(url, data=xml_data, headers=headers)
        return resp
