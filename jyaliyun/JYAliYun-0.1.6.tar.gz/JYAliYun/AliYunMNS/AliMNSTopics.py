#! /usr/bin/env python
# coding: utf-8

import base64
from JYAliYun import XML_CONTENT
from JYAliYun.Tools import jy_requests
from JYAliYun.Tools import ConvertObject
from JYAliYun.AliYunMNS import construct_headers
from JYAliYun.AliYunObject import ObjectManager

__author__ = 'ZhouHeng'


class MNSTopicsManager(ObjectManager):
    version = "2015-06-06"

    def __init__(self, topic_name, *args, **kwargs):
        kwargs["logger_name"] = "MNS_TOPICS_MESSAGE"
        super(MNSTopicsManager, self).__init__(*args, **kwargs)
        self.topic_name = topic_name
        self.message_tag = None
        self.message_attributes = None

    def publish_message(self, message_body, message_tag=None, message_attributes=None):
        self.info_log("PUBLISH MESSAGE [%s] %s" % (message_tag, message_body))
        message_body = base64.b64encode(ConvertObject.encode(message_body))
        data = {"MessageBody": message_body}
        if message_tag is not None:
            data["MessageTag"] = message_tag
        if message_attributes is not None:
            data["MessageAttributes"] = message_attributes
        resource = "/topics/%s/messages" % self.topic_name
        headers = construct_headers(self.access_key_id, self.access_key_secret, "POST", XML_CONTENT,
                                    {"x-mns-version": self.version}, resource)

        xml_data = ConvertObject.dict_to_xml("Message", data)
        url = self.server_url + resource
        resp = jy_requests.post(url, data=xml_data, headers=headers)
        if resp.status_code / 100 != 2:
            self.waring_log("PUBLISH MESSAGE [%s] %s" % (message_tag, message_body),
                            "RETURN %s %s" % (resp.status_code, resp.text))
        return resp
